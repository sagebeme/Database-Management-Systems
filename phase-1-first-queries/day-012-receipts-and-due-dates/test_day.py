"""Day 12: Receipts and Due Dates."""

import pytest


@pytest.fixture
def shop(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def got(db, path, columns):
    result = db.run_file(path).check()
    assert result.columns == columns
    return result.rows


def test_receipt_lines(shop, target):
    lines = [line for (line,) in got(shop, target / "0-receipt_lines.sql", ["line"])]
    assert lines == [
        "FATMA SAID: KES 18,500.00", "JUMA MWINYI: KES 2,750.50", "REHEMA ALI: KES 12,000.00",
        "OMAR BAKARI: KES 4,300.00", "FATMA SAID: KES 6,800.00", "ZUHURA MOHAMED: KES 9,500.00",
        "JUMA MWINYI: KES 15,250.00",
    ]


def test_first_names(shop, target):
    rows = got(shop, target / "1-first_names.sql", ["id", "first_name"])
    assert [name for _, name in rows] == ["Fatma", "Juma", "Rehema", "Omar", "Fatma", "Zuhura", "Juma"]


def test_first_name_of_a_three_part_name(shop, target):
    shop.run("INSERT INTO invoices VALUES (8, 'Mwanaisha Binti Salim', 'Stickers', 500, '2025-03-20', 7, NULL);").check()
    rows = got(shop, target / "1-first_names.sql", ["id", "first_name"])
    assert rows[-1] == ("8", "Mwanaisha")


def test_due_dates(shop, target):
    rows = got(shop, target / "2-due_dates.sql", ["id", "due_on"])
    assert rows == [("1", "2025-01-20"), ("2", "2025-01-27"), ("3", "2025-03-05"), ("4", "2025-02-24"),
                    ("5", "2025-03-14"), ("6", "2025-03-12"), ("7", "2025-04-16")]


def test_days_late(shop, target):
    assert got(shop, target / "3-days_late.sql", ["id", "days_late"]) == [("2", "7"), ("5", "6")]


def test_status(shop, target):
    rows = got(shop, target / "4-status.sql", ["id", "status"])
    assert rows == [("1", "on time"), ("2", "late"), ("3", "unpaid"), ("4", "on time"),
                    ("5", "late"), ("6", "unpaid"), ("7", "on time")], \
        "invoice 4 was paid on its due date, which is on time"


def test_kata_invoices_per_month(shop, target):
    assert got(shop, target / "kata.sql", ["month", "invoices"]) == [("2025-01", "2"), ("2025-02", "3"), ("2025-03", "2")]
