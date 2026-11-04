"""Day 98: a log-structured key-value store, the way Bitcask (Riak's storage engine) works.

Every write is appended to the end of the active segment file; nothing is ever changed in place.
An in-memory index maps each key to where its newest value sits on disk, so a read is one seek.
Old segments fill up with values nobody can see any more; compaction copies the live ones out.

    store = KV("data/")
    store.put("254712345678", b"Wanjiku")
    store.get("254712345678")      # b"Wanjiku"
    store.delete("254712345678")
    store.close()
"""

from __future__ import annotations

import os
import struct
import zlib
from dataclasses import dataclass
from pathlib import Path

HEADER = struct.Struct("<IIi")  # crc32, key length, value length (-1 means deleted)
TOMBSTONE = -1


class CorruptError(Exception):
    """A record in the middle of the data doesn't match its checksum."""


@dataclass(frozen=True)
class Where:
    segment: int
    offset: int  # where the value's bytes start
    size: int


def encode(key: str, value: bytes | None) -> bytes:
    """Done for you: one record, ready to append."""
    k = key.encode()
    v = b"" if value is None else value
    body = HEADER.pack(0, len(k), TOMBSTONE if value is None else len(v))[4:] + k + v
    return struct.pack("<I", zlib.crc32(body)) + body


def read_records(path: Path):
    """Done for you: yields (offset, key, value or None, record length) for each whole, valid record.
    Stops at the first torn or corrupt record and yields ("bad", offset) instead, then ends."""
    data = path.read_bytes()
    pos = 0
    while pos < len(data):
        if pos + HEADER.size > len(data):
            yield ("bad", pos)
            return
        crc, klen, vlen = HEADER.unpack_from(data, pos)
        end = pos + HEADER.size + klen + max(vlen, 0)
        if end > len(data) or zlib.crc32(data[pos + 4:end]) != crc:
            yield ("bad", pos)
            return
        key = data[pos + HEADER.size:pos + HEADER.size + klen].decode()
        value = None if vlen == TOMBSTONE else data[pos + HEADER.size + klen:end]
        yield (pos, key, value, end - pos)
        pos = end


def segment_name(number: int) -> str:
    return f"{number:06d}.log"


class KV:
    def __init__(self, directory: str | os.PathLike, max_segment_bytes: int = 1 << 20):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.max_segment_bytes = max_segment_bytes
        self.index: dict[str, Where] = {}
        self._load()

    def segments(self) -> list[int]:
        """Done for you: segment numbers on disk, oldest first."""
        return sorted(int(p.stem) for p in self.dir.glob("*.log") if p.stem.isdigit())

    def _path(self, number: int) -> Path:
        return self.dir / segment_name(number)

    def _load(self) -> None:
        """Rebuild the index by reading every segment, oldest first: a later record for a key wins,
        and a tombstone removes it. A torn record at the end of the newest segment (a crash mid-write)
        is cut off; a bad record anywhere else raises CorruptError. Then open the active segment."""
        numbers = self.segments()
        for number in numbers:
            for record in read_records(self._path(number)):
                if record[0] == "bad":
                    if number != numbers[-1]:
                        raise CorruptError(f"{segment_name(number)} is damaged at byte {record[1]}")
                    with open(self._path(number), "r+b") as f:
                        f.truncate(record[1])
                    break
                offset, key, value, length = record
                if value is None:
                    self.index.pop(key, None)
                else:
                    self.index[key] = Where(number, offset + length - len(value), len(value))
        self.active = numbers[-1] if numbers else 1
        self.file = open(self._path(self.active), "ab")

    def _append(self, key: str, value: bytes | None) -> int:
        """Append one record to the active segment, starting a new segment first if this one is full.
        Returns the record's offset."""
        if self.file.tell() >= self.max_segment_bytes:
            self.file.close()
            self.active += 1
            self.file = open(self._path(self.active), "ab")
        offset = self.file.tell()
        self.file.write(encode(key, value))
        self.file.flush()
        return offset

    def put(self, key: str, value: bytes) -> None:
        if not isinstance(value, bytes):
            raise TypeError("values are bytes")
        offset = self._append(key, value)
        size = len(value)
        self.index[key] = Where(self.active, offset + HEADER.size + len(key.encode()), size)

    def get(self, key: str) -> bytes | None:
        where = self.index.get(key)
        if where is None:
            return None
        with open(self._path(where.segment), "rb") as f:
            f.seek(where.offset)
            return f.read(where.size)

    def delete(self, key: str) -> bool:
        """Write a tombstone; True if the key existed."""
        if key not in self.index:
            return False
        self._append(key, None)
        del self.index[key]
        return True

    def keys(self) -> list[str]:
        return sorted(self.index)

    def compact(self) -> None:
        """Copy every live value into new segments numbered after all the existing ones, then delete
        the old segments. The data must be safe at every moment: write and fsync the new segments
        completely before removing anything. (If the power goes off in between, the old and new
        copies hold the same values, and the newer ones win on the next load.) The last new segment
        becomes the active one."""
        old = self.segments()
        self.file.close()
        number = old[-1] + 1
        out = open(self._path(number), "ab")
        moved = {}
        for _, _, key in sorted((w.segment, w.offset, k) for k, w in self.index.items()):
            if out.tell() >= self.max_segment_bytes:
                out.close()
                number += 1
                out = open(self._path(number), "ab")
            value = self.get(key)
            offset = out.tell()
            out.write(encode(key, value))
            moved[key] = Where(number, offset + HEADER.size + len(key.encode()), len(value))
        out.flush()
        os.fsync(out.fileno())
        out.close()
        self.index = moved
        for n in old:
            self._path(n).unlink()
        self.active = number
        self.file = open(self._path(self.active), "ab")

    def dead_ratio(self) -> float:
        """The kata: the share of bytes on disk that hold nothing a reader can see (old values,
        tombstones, record headers of dead records). 0.0 for an empty store."""
        total = sum(self._path(n).stat().st_size for n in self.segments())
        if total == 0:
            return 0.0
        live = sum(HEADER.size + len(k.encode()) + w.size for k, w in self.index.items())
        return (total - live) / total

    def maybe_compact(self, threshold: float = 0.5) -> bool:
        """The kata: compact when more than `threshold` of the bytes are dead. True if it did."""
        if self.dead_ratio() <= threshold:
            return False
        self.compact()
        return True

    def close(self) -> None:
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
