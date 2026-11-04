"""Day 18: Towns in Nakuru."""

import pytest


@pytest.fixture
def places(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def got(db, path, columns):
    result = db.run_file(path).check()
    assert result.columns == columns
    return result.rows


def test_towns_in_nakuru(places, target):
    assert got(places, target / "0-towns_in_nakuru.sql", ["id", "name"]) == [
        ("9", "Nakuru"), ("10", "Naivasha"), ("11", "Molo"), ("14", "Gilgil"),
    ]


def test_towns_in_nakuru_looks_up_the_county(places, target):
    places.run("UPDATE counties SET name = 'Nakuru (old)' WHERE id = 5; "
               "UPDATE counties SET name = 'Nakuru' WHERE id = 7;").check()
    assert got(places, target / "0-towns_in_nakuru.sql", ["id", "name"]) == [("15", "Nairobi")]


def test_shops_in_kiambu(places, target):
    assert got(places, target / "1-shops_in_kiambu.sql", ["name"]) == [
        ("Limuru Tea Room",), ("Ruiru Boutique",), ("Thika Road Spares",),
    ]


def test_above_average(places, target):
    rows = got(places, target / "2-above_average.sql", ["name", "monthly_sales"])
    assert rows[0] == ("Gilgil Mechanics", "394000")
    assert len(rows) == 8


def test_above_average_follows_the_data(places, target):
    places.run("UPDATE shops SET monthly_sales = 5000000 WHERE name = 'Westgate Books';").check()
    rows = got(places, target / "2-above_average.sql", ["name", "monthly_sales"])
    assert rows == [("Westgate Books", "5000000")], "with one huge shop, only it beats the average"


def test_towns_without_shops(places, target):
    assert got(places, target / "3-towns_without_shops.sql", ["name"]) == [("Athi River",), ("Kikuyu",), ("Maseno",)]


def test_top_shop_per_town(places, target):
    want = places.run(
        "SELECT town_id, name, monthly_sales FROM shops s WHERE monthly_sales = "
        "(SELECT MAX(monthly_sales) FROM shops WHERE town_id = s.town_id) ORDER BY town_id;").check().rows
    rows = got(places, target / "4-top_shop_per_town.sql", ["town_id", "name", "monthly_sales"])
    assert rows == want
    assert ("10", "Lakeside Hardware", "378000") in rows


def test_kata_average_town(places, target):
    # 12 towns have shops; their totals add up to 4,099,000.
    assert got(places, target / "kata.sql", ["avg_town_sales"]) == [("341583",)]
