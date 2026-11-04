"""Day 10: Best-Selling Saccos."""

import pytest


@pytest.fixture
def trips(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def got(db, path, columns):
    result = db.run_file(path).check()
    assert result.columns == columns
    return result.rows


def test_busy_saccos(trips, target):
    assert got(trips, target / "0-busy_saccos.sql", ["sacco", "trips"]) == [("Neema Line", "20"), ("Kasi Sacco", "18")]


def test_busy_saccos_follows_the_data(trips, target):
    trips.run("DELETE FROM trips WHERE sacco = 'Kasi Sacco' AND id % 3 = 0;").check()
    left = trips.run("SELECT COUNT(*) FROM trips WHERE sacco = 'Kasi Sacco';").check().rows[0][0]
    rows = got(trips, target / "0-busy_saccos.sql", ["sacco", "trips"])
    assert ("Kasi Sacco" in [s for s, _ in rows]) == (int(left) >= 15)


def test_big_earners(trips, target):
    assert got(trips, target / "1-big_earners.sql", ["sacco", "revenue"]) == [("Neema Line", "19070"), ("Kasi Sacco", "13500")]


def test_full_routes(trips, target):
    assert got(trips, target / "2-full_routes.sql", ["route_no", "avg_passengers"]) == [("11", "10.7"), ("57", "9.9")]


def test_full_trips_counts_only_full_trips(trips, target):
    rows = got(trips, target / "3-full_trips.sql", ["sacco", "full_trips"])
    assert rows == [("Kasi Sacco", "10"), ("Neema Line", "10")], \
        "Umoja Express has 14 trips but only 7 full ones: filter trips with WHERE before grouping"


def test_top_two_routes(trips, target):
    assert got(trips, target / "4-top_two_routes.sql", ["route_no", "passengers"]) == [("11", "118"), ("45", "99")]


def test_kata_shared_routes(trips, target):
    assert got(trips, target / "kata.sql", ["route_no", "saccos"]) == [("11", "2"), ("23", "2"), ("42", "2"), ("45", "2")]
