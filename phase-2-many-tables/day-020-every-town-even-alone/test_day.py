"""Day 20: Every Town, Even Alone."""

import pytest

SHOP_COUNTS = (
    "SELECT t.name AS town, COUNT(s.id) AS shops FROM towns t LEFT JOIN shops s ON s.town_id = t.id "
    "GROUP BY t.id, t.name ORDER BY shops DESC, town;"
)


@pytest.fixture
def places(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def got(db, path, columns):
    result = db.run_file(path).check()
    assert result.columns == columns
    return result.rows


def code_of(path):
    return " ".join(l for l in path.read_text().splitlines() if not l.strip().startswith("--")).upper()


def test_towns_and_their_shops(places, target):
    rows = got(places, target / "0-towns_and_their_shops.sql", ["town", "shop"])
    assert len(rows) == 21, "18 shops, plus one row each for the 3 towns with none"
    assert ("Athi River", "NULL") in rows and ("Maseno", "NULL") in rows
    assert rows[:2] == [("Athi River", "NULL"), ("Eldoret", "Eldoret Grains")]


def test_shop_counts(places, target):
    rows = got(places, target / "1-shop_counts.sql", ["town", "shops"])
    assert rows == places.run(SHOP_COUNTS).check().rows
    assert rows[0] == ("Naivasha", "3")
    assert rows[-3:] == [("Athi River", "0"), ("Kikuyu", "0"), ("Maseno", "0")]


def test_towns_without_shops(places, target):
    assert got(places, target / "2-towns_without_shops.sql", ["town"]) == [("Athi River",), ("Kikuyu",), ("Maseno",)]
    assert "JOIN" in code_of(target / "2-towns_without_shops.sql"), "today, find them with a join"


def test_right_join(places, target):
    assert got(places, target / "3-right_join.sql", ["town", "shops"]) == places.run(SHOP_COUNTS).check().rows
    assert "RIGHT JOIN" in code_of(target / "3-right_join.sql")


def test_towns_and_drivers(places, target):
    rows = got(places, target / "4-towns_and_drivers.sql", ["town", "driver"])
    assert ("NULL", "Joy Wanjiku") in rows and ("NULL", "Lucy Nyambura") in rows, "drivers with no town"
    assert ("Kikuyu", "NULL") in rows, "towns with no driver"
    assert ("Mombasa", "Ali Juma") in rows and ("Mombasa", "Hassan Abdi") in rows
    assert len(rows) == 18, "11 towns with no driver, 5 driver-town pairs, 2 drivers with no town"
    assert rows[-2:] == [("NULL", "Joy Wanjiku"), ("NULL", "Lucy Nyambura")]
    assert rows[0] == ("Athi River", "NULL")


def test_kata_empty_counties(places, target):
    assert got(places, target / "kata.sql", ["county"]) == [("Turkana",)]
