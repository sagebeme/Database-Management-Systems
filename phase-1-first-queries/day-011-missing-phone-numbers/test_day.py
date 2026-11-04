"""Day 11: Missing Phone Numbers."""

import pytest


@pytest.fixture
def shop(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def got(db, path, columns):
    result = db.run_file(path).check()
    assert result.columns == columns
    return result.rows


def test_no_phone(shop, target):
    assert got(shop, target / "0-no_phone.sql", ["name"]) == [
        ("Barasa Makokha",), ("Kiprotich Rono",), ("Mutiso Kilonzo",), ("Omari Hassan",),
    ]


def test_best_contact(shop, target):
    assert got(shop, target / "1-best_contact.sql", ["name", "contact"]) == [
        ("Achola Owino", "254711000007"),
        ("Barasa Makokha", "no contact"),
        ("Chepchumba Koech", "254711000005"),
        ("Kiprotich Rono", "kiprotich@example.com"),
        ("Mutiso Kilonzo", "mutiso@example.com"),
        ("Nasimiyu Wafula", "254711000003"),
        ("Omari Hassan", "no contact"),
        ("Wanjiku Kamau", "254711000001"),
    ]


def test_what_we_know(shop, target):
    assert got(shop, target / "2-what_we_know.sql", ["customers", "with_phone", "with_email"]) == [("8", "4", "4")]


def test_average_credit(shop, target):
    # Known limits: 50000, 20000, 10000, 30000, 0  -> 110000 / 5 = 22000
    # Unknown as zero: 110000 / 8 = 13750
    assert got(shop, target / "3-average_credit.sql", ["avg_known", "avg_unknown_as_zero"]) == [("22000.00", "13750.00")]


def test_not_referred_by_wanjiku(shop, target):
    names = [n for (n,) in got(shop, target / "4-not_referred_by_wanjiku.sql", ["name"])]
    assert names == ["Achola Owino", "Barasa Makokha", "Chepchumba Koech", "Mutiso Kilonzo", "Omari Hassan", "Wanjiku Kamau"], \
        "referred_by <> 1 is unknown (not true) when referred_by is NULL, so those rows need IS NULL too"


def test_kata_unknowns_last(shop, target):
    assert got(shop, target / "kata.sql", ["name", "credit_limit"]) == [
        ("Wanjiku Kamau", "50000.00"),
        ("Chepchumba Koech", "30000.00"),
        ("Kiprotich Rono", "20000.00"),
        ("Omari Hassan", "10000.00"),
        ("Achola Owino", "0.00"),
        ("Barasa Makokha", "NULL"),
        ("Mutiso Kilonzo", "NULL"),
        ("Nasimiyu Wafula", "NULL"),
    ]
