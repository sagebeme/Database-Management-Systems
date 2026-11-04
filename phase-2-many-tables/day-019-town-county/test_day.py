"""Day 19: Town, County."""

import pytest


@pytest.fixture
def places(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def got(db, path, columns):
    result = db.run_file(path).check()
    assert result.columns == columns
    return result.rows


def test_towns_and_counties(places, target):
    rows = got(places, target / "0-towns_and_counties.sql", ["id", "town", "county"])
    assert len(rows) == 15
    assert rows[:3] == [("1", "Mombasa", "Mombasa"), ("2", "Machakos", "Machakos"), ("3", "Athi River", "Machakos")]
    assert rows[13] == ("14", "Gilgil", "Nakuru")


def test_shops_and_towns(places, target):
    rows = got(places, target / "1-shops_and_towns.sql", ["shop", "town", "monthly_sales"])
    assert len(rows) == 18
    assert rows[0] == ("Gilgil Mechanics", "Gilgil", "394000")
    assert rows[-1] == ("Kilimo Agrovet", "Naivasha", "102000")


def test_shops_towns_counties(places, target):
    want = places.run(
        "SELECT s.name AS shop, t.name AS town, c.name AS county FROM shops s JOIN towns t ON s.town_id = t.id "
        "JOIN counties c ON t.county_id = c.id ORDER BY county, shop;").check().rows
    assert got(places, target / "2-shops_towns_counties.sql", ["shop", "town", "county"]) == want


def test_sales_per_county(places, target):
    rows = got(places, target / "3-sales_per_county.sql", ["county", "sales"])
    assert rows[0] == ("Nakuru", "1778000")
    assert len(rows) == 7


def test_neighbours_of_naivasha(places, target):
    assert got(places, target / "4-neighbours_of_naivasha.sql", ["name"]) == [("Gilgil",), ("Molo",), ("Nakuru",)]


def test_neighbours_follow_the_data(places, target):
    places.run("UPDATE towns SET county_id = 3 WHERE name = 'Naivasha';").check()
    assert got(places, target / "4-neighbours_of_naivasha.sql", ["name"]) == [
        ("Kikuyu",), ("Limuru",), ("Ruiru",), ("Thika",),
    ]


def test_kata_same_name(places, target):
    assert got(places, target / "kata.sql", ["town"]) == [
        ("Kisumu",), ("Machakos",), ("Mombasa",), ("Nairobi",), ("Nakuru",),
    ]
