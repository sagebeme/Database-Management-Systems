"""Day 29: The Exercise Book Problem."""

import threading

import pytest

from coursekit import load_module


@pytest.fixture
def book(target):
    return load_module(target / "book.py")


@pytest.fixture
def files(tmp_path):
    members, contributions = tmp_path / "members.csv", tmp_path / "contributions.csv"
    members.write_text("id,name,phone\n1,Wanjiku,254711000001\n2,Otieno,254722000002\n3,Chebet,254733000003\n")
    contributions.write_text("member_id,month,amount\n1,2026-09,1000\n2,2026-09,1000\n1,2026-10,1500\n"
                             "7,2026-10,500\n2,2026-10,1000\n9,2026-10,300\n")
    return members, contributions


def test_add_member_makes_the_file(book, tmp_path):
    path = tmp_path / "members.csv"
    assert book.add_member(path, "Wanjiku", "254711000001") == 1
    assert book.add_member(path, "Otieno", "254722000002") == 2
    assert path.read_text().splitlines() == ["id,name,phone", "1,Wanjiku,254711000001", "2,Otieno,254722000002"]


def test_add_member_continues_after_the_biggest_id(book, files):
    members, _ = files
    members.write_text("id,name,phone\n4,Achieng,254700000004\n2,Otieno,254722000002\n")
    assert book.add_member(members, "Kamau", "254799000009") == 5


def test_phones_are_unique(book, files):
    members, _ = files
    with pytest.raises(ValueError):
        book.add_member(members, "Impostor", "254722000002")
    assert len(members.read_text().splitlines()) == 4, "a refused member mustn't be written"


def test_find_by_phone(book, files):
    members, _ = files
    assert book.find_by_phone(members, "254733000003") == {"id": "3", "name": "Chebet", "phone": "254733000003"}
    assert book.find_by_phone(members, "254700000000") is None


def test_totals(book, files):
    assert book.totals(*files) == {"Wanjiku": 2500, "Otieno": 2000, "Chebet": 0}


def test_orphans(book, files):
    assert book.orphans(*files) == [
        {"member_id": "7", "month": "2026-10", "amount": "500"},
        {"member_id": "9", "month": "2026-10", "amount": "300"},
    ]


def test_rename(book, files):
    members, _ = files
    book.rename(members, 2, "Otieno Odhiambo")
    assert book.find_by_phone(members, "254722000002")["name"] == "Otieno Odhiambo"
    assert book.find_by_phone(members, "254711000001")["name"] == "Wanjiku"
    assert not members.with_name("members.csv.tmp").exists(), "the temporary file should be gone"
    with pytest.raises(KeyError):
        book.rename(members, 99, "Nobody")


def test_kata_two_treasurers(book, tmp_path):
    path = tmp_path / "members.csv"
    start = threading.Barrier(16)
    ids, errors = [], []

    def treasurer(n):
        start.wait()
        try:
            ids.append(book.add_member_locked(path, f"Member {n}", f"2547000000{n:02d}"))
        except Exception as e:  # noqa: BLE001 - reported below
            errors.append(e)

    threads = [threading.Thread(target=treasurer, args=(n,)) for n in range(16)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors, errors[0]
    assert sorted(ids) == list(range(1, 17)), "every member gets a different id"
    assert len(path.read_text().splitlines()) == 17
