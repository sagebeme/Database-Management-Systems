"""Day 78 capstone: The SACCO Engine."""

import random

import pytest

from coursekit import load_module


@pytest.fixture
def e(target):
    return load_module(target / "engine.py")


def member(i):
    return (i, f"2547{(i * 7919) % 10**8:08d}", f"Member {i}", (i * 37) % 250000)


def test_pack_and_unpack(e):
    row = (7, "254712345678", "Wanjiku Kamau", 15000)
    data = e.pack(row)
    assert isinstance(data, bytes) and len(data) == e.ROW.size == 54
    assert e.unpack(data) == row
    assert e.unpack(bytearray(data)) == row
    assert e.unpack(e.pack((-1, "254700000000", "", -500))) == (-1, "254700000000", "", -500)
    assert e.unpack(e.pack((1, "254700000000", "Njoroge Wa Mūkami", 0)))[2] == "Njoroge Wa Mūkami"


@pytest.mark.parametrize("row", [
    (1, "0712345678", "Short phone", 0),
    (1, "254712345678", "A name that is far too long to fit", 0),
    (1, "254712345678", "Ūūūūūūūūūūūūūūūū", 0),
])
def test_pack_refuses(e, row):
    with pytest.raises(ValueError):
        e.pack(row)


def test_heap_file(e, tmp_path):
    pages = e.Pages(tmp_path / "h.heap")
    heap = e.HeapFile(pages)
    rids = [heap.insert(member(i)) for i in range(1, 201)]
    assert e.ROWS_PER_PAGE == 75
    assert rids[0] == (0, 0) and rids[74] == (0, 74) and rids[75] == (1, 0) and rids[-1] == (2, 49)
    assert pages.count() == 3
    pages.reads = 0
    assert heap.get((1, 3)) == member(79)
    assert pages.reads == 1, "get reads exactly one page"
    assert [row for _, row in heap.scan()] == [member(i) for i in range(1, 201)]
    heap.put((2, 0), (151, "254700000151", "Changed", 1))
    assert heap.get((2, 0)) == (151, "254700000151", "Changed", 1)
    with pytest.raises(IndexError):
        heap.get((2, 50))
    with pytest.raises(IndexError):
        heap.get((3, 0))


def test_heap_survives_reopening(e, tmp_path):
    heap = e.HeapFile(e.Pages(tmp_path / "h.heap"))
    for i in range(1, 80):
        heap.insert(member(i))
    again = e.HeapFile(e.Pages(tmp_path / "h.heap"))
    assert again.get((1, 3)) == member(79)
    assert again.insert(member(80)) == (1, 4)


def test_table(e, tmp_path):
    t = e.Table(tmp_path / "sacco")
    order = list(range(1, 501))
    random.Random(78).shuffle(order)
    for i in order:
        t.insert(member(i))
    t.pages.reads = 0
    assert t.get(321) == member(321)
    assert t.pages.reads == 1, "the index is in memory: one page read for the row"
    assert t.get(999) is None
    assert t.range(10, 15) == [member(i) for i in range(10, 16)]
    assert t.range(498, 600) == [member(498), member(499), member(500)]
    with pytest.raises(ValueError):
        t.insert(member(321))
    with pytest.raises(ValueError):
        t.insert((1000, "07123", "Bad phone", 0))
    assert t.get(1000) is None, "a refused row leaves no trace"


def test_reopen_rebuilds_the_index(e, tmp_path):
    t = e.Table(tmp_path / "sacco")
    for i in range(1, 301):
        t.insert(member(i))
    t2 = e.Table(tmp_path / "sacco")
    assert t2.get(150) == member(150)
    assert t2.range(1, 300) == [member(i) for i in range(1, 301)]
    assert t2.pages.count() == 4, "reopening must not write the rows again"
    with pytest.raises(ValueError):
        t2.insert(member(5))


def test_log_comes_first(e, tmp_path):
    t = e.Table(tmp_path / "sacco")
    t.insert(member(1))
    seen = []
    t.log.append = lambda record: seen.append(("log", record))
    original = t.pages.write_page
    t.pages.write_page = lambda n, data: (seen.append(("page", n)), original(n, data))
    t.insert(member(2))
    assert [kind for kind, _ in seen] == ["log", "page"], "write-ahead: the log record before the page"


def test_power_cut_after_logging(e, tmp_path):
    t = e.Table(tmp_path / "sacco")
    for i in range(1, 75):
        t.insert(member(i))

    def power_cut(n, data):
        raise OSError("KPLC strikes again")

    t.pages.write_page = power_cut
    with pytest.raises(OSError):
        t.insert(member(75))
    t2 = e.Table(tmp_path / "sacco")
    assert t2.get(75) == member(75), "the insert was logged, so recovery must redo it"
    t3 = e.Table(tmp_path / "sacco")
    assert t3.range(1, 100) == [member(i) for i in range(1, 76)], "and recovering again changes nothing"
    assert t3.pages.count() == 1


def test_power_cut_before_logging(e, tmp_path):
    t = e.Table(tmp_path / "sacco")
    t.insert(member(1))

    def power_cut(record):
        raise OSError("KPLC strikes again")

    t.log.append = power_cut
    with pytest.raises(OSError):
        t.insert(member(2))
    assert e.Table(tmp_path / "sacco").get(2) is None, "nothing logged, so nothing may reach the page"


def test_kata_update_savings(e, tmp_path):
    t = e.Table(tmp_path / "sacco")
    for i in range(1, 101):
        t.insert(member(i))
    t.update_savings(42, 99_000)
    t.update_savings(42, 120_500)
    assert t.get(42) == (42, member(42)[1], "Member 42", 120_500)
    with pytest.raises(KeyError):
        t.update_savings(4242, 1)
    assert e.Table(tmp_path / "sacco").get(42)[3] == 120_500
    t2 = e.Table(tmp_path / "sacco")
    t2.pages.write_page = lambda n, data: (_ for _ in ()).throw(OSError("KPLC"))
    with pytest.raises(OSError):
        t2.update_savings(7, 5)
    t3 = e.Table(tmp_path / "sacco")
    assert t3.get(7)[3] == 5, "a logged update survives a power cut"
    assert t3.get(42)[3] == 120_500, "redo applies updates in log order: the last one wins"
    assert e.Table(tmp_path / "sacco").range(1, 100)[6][3] == 5
