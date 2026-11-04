"""Day 98: Portfolio: Build a Key-Value Store."""

import os
from pathlib import Path

import pytest

from coursekit import load_module


@pytest.fixture
def kv(target):
    return load_module(target / "kv.py")


@pytest.fixture
def store(kv, tmp_path):
    s = kv.KV(tmp_path)
    yield s
    s.close()


def disk_bytes(folder):
    return sum(p.stat().st_size for p in Path(folder).glob("*.log"))


def test_put_get_delete(kv, store):
    assert store.get("254712345678") is None
    store.put("254712345678", b"Wanjiku")
    store.put("254722000111", b"Otieno")
    store.put("254712345678", b"Wanjiku Kamau")
    assert store.get("254712345678") == b"Wanjiku Kamau"
    assert store.get("254722000111") == b"Otieno"
    store.put("empty", b"")
    assert store.get("empty") == b""
    store.put("jina", "Zawadi ✓".encode())
    assert store.get("jina").decode() == "Zawadi ✓"
    assert store.delete("254722000111") is True
    assert store.delete("254722000111") is False
    assert store.get("254722000111") is None
    assert store.keys() == ["254712345678", "empty", "jina"]
    with pytest.raises(TypeError):
        store.put("x", "not bytes")
    assert all(isinstance(w, kv.Where) for w in store.index.values()), "the index holds where values live"


def test_append_only(store, tmp_path):
    store.put("a", b"first")
    before = (tmp_path / "000001.log").read_bytes()
    store.put("a", b"second")
    store.delete("a")
    after = (tmp_path / "000001.log").read_bytes()
    assert after.startswith(before) and len(after) > len(before), "writes only ever append"


def test_reopen(kv, tmp_path):
    with kv.KV(tmp_path) as s:
        for i in range(50):
            s.put(f"k{i}", f"v{i}".encode())
        s.put("k7", b"changed")
        s.delete("k8")
    with kv.KV(tmp_path) as s:
        assert s.get("k7") == b"changed"
        assert s.get("k8") is None, "a delete must survive a restart"
        assert s.get("k49") == b"v49"
        assert len(s.keys()) == 49
        s.put("k8", b"back")
    with kv.KV(tmp_path) as s:
        assert s.get("k8") == b"back"


def test_segments_roll(kv, tmp_path):
    with kv.KV(tmp_path, max_segment_bytes=200) as s:
        for i in range(40):
            s.put(f"key{i:02d}", b"x" * 30)
        assert s.segments() == list(range(1, len(s.segments()) + 1))
        assert len(s.segments()) >= 6
        for n in s.segments()[:-1]:
            assert (tmp_path / f"{n:06d}.log").stat().st_size < 200 + 60, "start a new segment once one is full"
        s.put("key00", b"newest")
        assert s.get("key00") == b"newest"
    with kv.KV(tmp_path, max_segment_bytes=200) as s:
        assert s.get("key00") == b"newest", "the newest segment wins on reload"
        assert s.get("key39") == b"x" * 30


def test_torn_write(kv, tmp_path):
    with kv.KV(tmp_path) as s:
        s.put("a", b"apple")
        s.put("b", b"banana")
    path = tmp_path / "000001.log"
    good = path.stat().st_size
    record = kv.encode("c", b"cherry")
    with open(path, "ab") as f:
        f.write(record[:-3])  # the power went off mid-write
    with kv.KV(tmp_path) as s:
        assert s.get("c") is None and s.get("b") == b"banana"
        assert path.stat().st_size == good, "cut the torn record off"
        s.put("c", b"cherry")
    with kv.KV(tmp_path) as s:
        assert s.get("c") == b"cherry"


def test_corruption_in_an_old_segment(kv, tmp_path):
    with kv.KV(tmp_path, max_segment_bytes=100) as s:
        for i in range(20):
            s.put(f"k{i}", b"value-%d" % i)
    first = tmp_path / "000001.log"
    data = bytearray(first.read_bytes())
    data[20] ^= 0xFF
    first.write_bytes(bytes(data))
    with pytest.raises(kv.CorruptError):
        kv.KV(tmp_path, max_segment_bytes=100)


def test_compact(kv, tmp_path):
    with kv.KV(tmp_path, max_segment_bytes=300) as s:
        for round_ in range(10):
            for i in range(10):
                s.put(f"k{i}", b"round %d" % round_)
        for i in range(5):
            s.delete(f"k{i}")
        before_segments = s.segments()
        before = disk_bytes(tmp_path)
        s.compact()
        after = disk_bytes(tmp_path)
        live = sum(len(kv.encode(k, s.get(k))) for k in s.keys())
        assert after == live, "after compaction the disk holds only the live records"
        assert after < before / 5
        assert min(s.segments()) > max(before_segments), "compacted segments come after the old ones"
        assert s.keys() == [f"k{i}" for i in range(5, 10)]
        assert s.get("k7") == b"round 9"
        s.put("k9", b"after")
        s.put("k0", b"reborn")
    with kv.KV(tmp_path, max_segment_bytes=300) as s:
        assert s.get("k9") == b"after"
        assert s.get("k0") == b"reborn"
        assert s.get("k1") is None, "a deleted key mustn't come back after compaction"
        assert s.get("k6") == b"round 9"


def test_compaction_crash_loses_nothing(kv, tmp_path, monkeypatch):
    with kv.KV(tmp_path, max_segment_bytes=120) as s:
        s.put("founder", b"only in the oldest segment")
        for i in range(30):
            s.put(f"k{i % 7}", b"v%d" % i)
        s.delete("k3")
        expected = {k: s.get(k) for k in s.keys()}

        deleted = []
        real_unlink = os.unlink

        def one_delete_then_power_cut(path, *args, **kwargs):
            """The first file deletion works; then the power goes off."""
            if deleted:
                raise OSError("power cut")
            deleted.append(str(path))
            return real_unlink(os.fspath(path))

        monkeypatch.setattr(Path, "unlink", one_delete_then_power_cut)
        monkeypatch.setattr(os, "remove", one_delete_then_power_cut)
        monkeypatch.setattr(os, "unlink", one_delete_then_power_cut)
        with pytest.raises(OSError, match="power cut"):
            s.compact()
        monkeypatch.undo()
        assert len(s.segments()) > 1
        s.file.close()
    with kv.KV(tmp_path, max_segment_bytes=120) as s:
        assert {k: s.get(k) for k in s.keys()} == expected, "write the new segments before deleting the old"


def test_kata_dead_ratio(kv, tmp_path):
    with kv.KV(tmp_path) as s:
        assert s.dead_ratio() == 0.0
        s.put("a", b"1234")
        assert s.dead_ratio() == 0.0
        s.put("a", b"5678")
        assert s.dead_ratio() == pytest.approx(0.5)
        assert s.maybe_compact(0.5) is False
        s.delete("a")
        assert s.dead_ratio() == 1.0
        s.put("b", b"x" * 50)
        assert s.maybe_compact(0.3) is True
        assert s.dead_ratio() == 0.0
        assert s.get("b") == b"x" * 50 and s.get("a") is None
