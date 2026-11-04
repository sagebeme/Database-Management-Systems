"""Day 27: Loading Real Data. The file paths in LOAD DATA are relative to the course folder,
so the tests run from there, as you do."""

import pytest

KNBS_TOTAL = "47564296"  # the published 2019 census total


@pytest.fixture
def course_root(day, monkeypatch):
    monkeypatch.chdir(day.parents[1])


@pytest.fixture
def counties(mysql, day, course_root):
    mysql.load(day / "reference.sql")
    return mysql


def test_counties_table(mysql, day, target, course_root):
    mysql.run_file(target / "0-counties_table.sql").check()
    mysql.run_file(target / "0-counties_table.sql").check()
    load = (day / "reference.sql").read_text().split("LOAD DATA", 1)[1]
    mysql.run("LOAD DATA" + load).check()
    rows = mysql.run("SELECT code, name, total_area_km2, land_area_km2, population "
                     "FROM counties WHERE code = '047';").check().rows
    assert rows == [("047", "Nairobi", "707", "707", "4397073")]
    assert not mysql.run("INSERT INTO counties VALUES ('047', 'X', 'Y', 'Z', 1, 1, 1);").ok, "code is the key"
    assert not mysql.run("INSERT INTO counties VALUES ('048', 'Nairobi', 'Y', 'Z', 1, 1, 1);").ok, "names are unique"
    assert not mysql.run("INSERT INTO counties (code, name) VALUES ('049', 'Q');").ok, "everything is required"


def test_load_counties(mysql, day, target, course_root):
    ddl = (day / "reference.sql").read_text().split("LOAD DATA", 1)[0]
    mysql.run(ddl).check()
    mysql.run_file(target / "1-load_counties.sql").check()
    got = mysql.run("SELECT COUNT(*), SUM(population), SUM(total_area_km2), SUM(land_area_km2) FROM counties;").check()
    assert got.rows == [("47", KNBS_TOTAL, "591971", "580609")], "47 counties, and the totals KNBS publishes"
    names = mysql.run("SELECT name FROM counties WHERE code IN ('006', '021') ORDER BY code;").check().column(0)
    assert names == ["Taita–Taveta", "Murang'a"], "quotes, apostrophes and the en dash must survive"
    assert mysql.run("SELECT capital, population FROM counties WHERE code = '023';").check().rows \
        == [("Lodwar", "926976")]


def test_check_the_load(counties, target):
    got = counties.run_file(target / "2-check_the_load.sql").check()
    assert got.columns == ["counties", "population"]
    assert got.rows == [("47", KNBS_TOTAL)]
    counties.run("DELETE FROM counties WHERE code = '047';").check()
    assert counties.run_file(target / "2-check_the_load.sql").check().rows == [("46", "43167223")]


def test_most_crowded(counties, target):
    got = counties.run_file(target / "3-most_crowded.sql").check()
    assert got.columns == ["county", "density"]
    assert got.rows == [("Mombasa", "8002"), ("Nairobi", "6219"), ("Vihiga", "1048"),
                        ("Kisii", "959"), ("Kiambu", "941")]
    counties.run("UPDATE counties SET land_area_km2 = 216 WHERE code = '001';").check()
    assert counties.run_file(target / "3-most_crowded.sql").check().rows[0] == ("Nairobi", "6219")


def test_province_totals(counties, target):
    got = counties.run_file(target / "4-province_totals.sql").check()
    assert got.columns == ["former_province", "counties", "population"]
    assert got.rows[0] == ("Rift Valley", "14", "12752966")
    assert got.rows[-1] == ("North Eastern", "3", "2490073")
    assert len(got.rows) == 8


def test_kata_counties_on_the_water(counties, target):
    got = counties.run_file(target / "kata.sql").check()
    assert got.columns == ["county", "water_percent"]
    assert got.rows == [("Homa Bay", "43.4"), ("Siaya", "30.7"), ("Mombasa", "30.1"), ("Kisumu", "21.2")]
