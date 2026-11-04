"""Day 78 capstone: the SACCO's own little storage engine.

A members table kept in a heap file of 4 KB pages, a B+ tree index on id held in memory, and a write-ahead log
so that a power cut never loses a change that was logged.

A row is (id, phone, name, savings): id and savings are integers, phone is 12 characters, name at most 30
bytes of UTF-8.

Files in the table's folder:
    members.heap   the pages
    wal.log        the log: one JSON record per line
"""

import json
import os
import struct
from pathlib import Path

from bplustree import BPlusTree

PAGE_SIZE = 4096
ROW = struct.Struct("<i12s30sq")       # 54 bytes: id, phone, name, savings
HEADER = struct.Struct("<H")           # 2 bytes at the start of each page: how many rows it holds
ROWS_PER_PAGE = (PAGE_SIZE - HEADER.size) // ROW.size
INDEX_ORDER = 64


class Pages:
    """A file of fixed-size pages. Counts every read and write so tests can see what you touch. (Done for you.)"""

    def __init__(self, path):
        self.path = Path(path)
        self.path.touch()
        self.reads = self.writes = 0

    def count(self):
        return self.path.stat().st_size // PAGE_SIZE

    def read_page(self, n):
        if not 0 <= n < self.count():
            raise IndexError(f"there's no page {n}")
        self.reads += 1
        with self.path.open("rb") as f:
            f.seek(n * PAGE_SIZE)
            return bytearray(f.read(PAGE_SIZE))

    def write_page(self, n, data):
        """Write page n (n == count() adds a new page at the end) and make sure it's on disk."""
        if len(data) != PAGE_SIZE:
            raise ValueError(f"a page is {PAGE_SIZE} bytes, not {len(data)}")
        if not 0 <= n <= self.count():
            raise IndexError(f"can't write page {n} of a {self.count()}-page file")
        self.writes += 1
        with self.path.open("r+b") as f:
            f.seek(n * PAGE_SIZE)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())


class Log:
    """An append-only log of JSON records, each forced to disk before append() returns. (Done for you.)"""

    def __init__(self, path):
        self.path = Path(path)
        self.path.touch()

    def append(self, record):
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
            f.flush()
            os.fsync(f.fileno())

    def records(self):
        with self.path.open(encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]


def pack(row):
    """A row as ROW.size bytes. Strings are UTF-8, padded with zero bytes. ValueError if phone isn't exactly 12
    characters or the name is over 30 bytes."""
    rid, phone, name, savings = row
    phone_b, name_b = phone.encode(), name.encode()
    if len(phone_b) != 12:
        raise ValueError(f"a phone is 12 characters: {phone!r}")
    if len(name_b) > 30:
        raise ValueError(f"names are at most 30 bytes: {name!r}")
    return ROW.pack(rid, phone_b, name_b, savings)


def unpack(data):
    """The row back from its bytes, without the padding."""
    rid, phone, name, savings = ROW.unpack(bytes(data))
    return rid, phone.rstrip(b"\0").decode(), name.rstrip(b"\0").decode(), savings


class HeapFile:
    """Rows in pages, in the order they arrive. A row's address (rid) is (page number, slot number)."""

    def __init__(self, pages):
        self.pages = pages

    def insert(self, row):
        """Put the row in the last page if it has room, otherwise in a new page. Return its rid."""
        n = self.pages.count() - 1
        page = self.pages.read_page(n) if n >= 0 else None
        if page is None or HEADER.unpack_from(page)[0] == ROWS_PER_PAGE:
            n, page = n + 1, bytearray(PAGE_SIZE)
        used = HEADER.unpack_from(page)[0]
        ROW.pack_into(page, HEADER.size + used * ROW.size, *ROW.unpack(pack(row)))
        HEADER.pack_into(page, 0, used + 1)
        self.pages.write_page(n, page)
        return n, used

    def get(self, rid):
        """The row at rid, reading exactly one page."""
        n, slot = rid
        page = self.pages.read_page(n)
        if not 0 <= slot < HEADER.unpack_from(page)[0]:
            raise IndexError(f"there's no row at {rid}")
        return unpack(page[HEADER.size + slot * ROW.size:HEADER.size + (slot + 1) * ROW.size])

    def put(self, rid, row):
        """Overwrite the row at rid in place."""
        n, slot = rid
        page = self.pages.read_page(n)
        if not 0 <= slot < HEADER.unpack_from(page)[0]:
            raise IndexError(f"there's no row at {rid}")
        page[HEADER.size + slot * ROW.size:HEADER.size + (slot + 1) * ROW.size] = pack(row)
        self.pages.write_page(n, page)

    def scan(self):
        """Every (rid, row), page by page, slot by slot."""
        for n in range(self.pages.count()):
            page = self.pages.read_page(n)
            for slot in range(HEADER.unpack_from(page)[0]):
                yield (n, slot), unpack(page[HEADER.size + slot * ROW.size:HEADER.size + (slot + 1) * ROW.size])


class Table:
    def __init__(self, folder):
        """Open (or create) the table in folder and recover: rebuild the index from the heap with
        BPlusTree.bulk_load, then redo every logged change the heap is missing."""
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        self.pages = Pages(folder / "members.heap")
        self.heap = HeapFile(self.pages)
        self.log = Log(folder / "wal.log")
        pairs = sorted((row[0], rid) for rid, row in self.heap.scan())
        self.index = BPlusTree.bulk_load(INDEX_ORDER, pairs)
        for record in self.log.records():
            if record["op"] == "insert":
                row = tuple(record["row"])
                if self.index.get(row[0]) is None:
                    self.index.insert(row[0], self.heap.insert(row))
            elif record["op"] == "update":
                self._set_savings(record["id"], record["savings"])

    def insert(self, row):
        """Add a row: ValueError if the id is taken or the row can't be packed. Log it, then write the page,
        then index it."""
        row = tuple(row)
        pack(row)
        if self.index.get(row[0]) is not None:
            raise ValueError(f"member {row[0]} already exists")
        self.log.append({"op": "insert", "row": list(row)})
        self.index.insert(row[0], self.heap.insert(row))

    def get(self, member_id):
        """The row with that id, or None, reading at most one page."""
        rid = self.index.get(member_id)
        return None if rid is None else self.heap.get(rid)

    def range(self, lo, hi):
        """Rows with lo <= id <= hi, in id order."""
        return [self.heap.get(rid) for _, rid in self.index.range(lo, hi)]

    def update_savings(self, member_id, savings):
        """Kata: set a member's savings. KeyError if there's no such member. Log first, then change the row in
        place; recovery redoes it, and redoing it twice must be harmless."""
        if self.index.get(member_id) is None:
            raise KeyError(member_id)
        self.log.append({"op": "update", "id": member_id, "savings": savings})
        self._set_savings(member_id, savings)

    def _set_savings(self, member_id, savings):
        """Change one member's savings in their page. (Part of the kata.)"""
        rid = self.index.get(member_id)
        if rid is None:
            return
        rid_, phone, name, _ = self.heap.get(rid)
        self.heap.put(rid, (rid_, phone, name, savings))
