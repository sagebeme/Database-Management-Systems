"""Day 57: Band Lifespans."""

import pytest

# A Taarab act tying with Nyota ya Pwani, a loan one day late from December, and a member born on 1 April.
SHAKE_UP = """INSERT INTO artists VALUES (21, 'Lamu Dhow Taarab', 'Taarab', 'Kenya', 90000, 1990, NULL);
INSERT INTO members VALUES (7, 'Zawadi Mwende', '2008-04-01');
INSERT INTO loans VALUES (11, 7, 'Mstahiki Meya', '2025-12-30', '2026-01-14');"""
QUERIES = ["0-lifespans", "1-due_dates", "2-overdue", "3-ages", "4-loans_per_month", "kata"]


@pytest.fixture
def library(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def run(db, folder, name):
    return db.run_file(folder / f"{name}.sql").check().rows


def test_lifespans(library, target):
    assert run(library, target, "0-lifespans") == [
        ("Unguja Strings", "54"), ("Nyota ya Pwani", "36"), ("Mombasa Taarab Ensemble", "31")]


def test_due_dates(library, target):
    rows = run(library, target, "1-due_dates")
    assert rows[0] == ("1", "2026-01-05", "2026-01-19", "Monday")
    assert rows[4] == ("5", "2026-02-14", "2026-02-28", "Saturday")
    assert rows[8] == ("9", "2026-03-20", "2026-04-03", "Friday"), "into the next month"


def test_overdue(library, target):
    assert run(library, target, "2-overdue") == [
        ("4", "Mutua Musyoka", "74", "500"), ("6", "Wanjiku Kamau", "25", "250"),
        ("2", "Otieno Ouma", "9", "90"), ("8", "Otieno Ouma", "7", "70")]


def test_ages(library, target):
    assert run(library, target, "3-ages") == [
        ("Mutua Musyoka", "47"), ("Otieno Ouma", "41"), ("Wanjiku Kamau", "35"), ("Hassan Ali", "27"),
        ("Chebet Rono", "22"), ("Akinyi Atieno", "15")]


def test_loans_per_month(library, target):
    assert run(library, target, "4-loans_per_month") == [("2026-01", "4"), ("2026-02", "2"), ("2026-03", "4")]


@pytest.mark.parametrize("name", QUERIES)
def test_on_other_data(library, day, target, name):
    library.run(SHAKE_UP).check()
    assert run(library, target, name) == run(library, day / "solution", name)


def test_kata_next_birthday(library, target):
    assert run(library, target, "kata") == [
        ("Otieno Ouma", "2026-03-31", "0"), ("Akinyi Atieno", "2026-04-01", "1"), ("Wanjiku Kamau", "2026-04-12", "12"),
        ("Mutua Musyoka", "2026-12-01", "245"), ("Chebet Rono", "2027-02-28", "334"), ("Hassan Ali", "2027-03-30", "364")]
