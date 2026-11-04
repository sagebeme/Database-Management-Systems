"""Day 17: Counties and Towns."""

import pytest


@pytest.fixture
def places(mysql, day, target):
    """Your two tables, filled with the day's data."""
    mysql.run_file(target / "0-counties_table.sql").check()
    mysql.run_file(target / "1-towns_table.sql").check()
    mysql.load(day / "data.sql")
    return mysql


def test_counties_table_rules(mysql, target):
    mysql.run_file(target / "0-counties_table.sql").check()
    assert mysql.run_file(target / "0-counties_table.sql").ok, "IF NOT EXISTS"
    mysql.run("INSERT INTO counties (code, name) VALUES ('030', 'Baringo');").check()
    assert mysql.run("SELECT id FROM counties;").check().rows == [("1",)], "id is numbered automatically"
    assert not mysql.run("INSERT INTO counties (code, name) VALUES ('030', 'Copy');").ok, "code is unique"
    assert not mysql.run("INSERT INTO counties (code, name) VALUES ('031', 'Baringo');").ok, "name is unique"
    assert not mysql.run("INSERT INTO counties (code, name) VALUES (NULL, 'Laikipia');").ok, "code is required"


def test_towns_must_belong_to_a_real_county(places):
    refused = places.run("INSERT INTO towns (county_id, name) VALUES (99, 'Atlantis');")
    assert not refused.ok and "foreign key constraint fails" in refused.stderr
    assert not places.run("INSERT INTO towns (county_id, name) VALUES (NULL, 'Nowhere');").ok, "county_id is required"


def test_a_county_with_towns_cannot_be_deleted(places):
    refused = places.run("DELETE FROM counties WHERE name = 'Nakuru';")
    assert not refused.ok, "the foreign key should stop a county with towns from being deleted"


def test_add_gilgil(places, target):
    places.run_file(target / "2-add_gilgil.sql").check()
    rows = places.run("SELECT county_id FROM towns WHERE name = 'Gilgil';").check().rows
    assert rows == [("5",)]


def test_add_gilgil_looks_up_the_id(places, target):
    places.run("UPDATE towns SET county_id = 7 WHERE county_id = 5; DELETE FROM counties WHERE id = 5; "
               "INSERT INTO counties (id, code, name) VALUES (50, '032', 'Nakuru');").check()
    places.run_file(target / "2-add_gilgil.sql").check()
    rows = places.run("SELECT county_id FROM towns WHERE name = 'Gilgil';").check().rows
    assert rows == [("50",)], "look Nakuru's id up by name; don't type 5"


def test_wards_go_with_their_town(places, target):
    places.run_file(target / "3-wards_table.sql").check()
    places.run("INSERT INTO wards (town_id, name) VALUES (10, 'Hells Gate'), (10, 'Lake View'), (9, 'Biashara');").check()
    assert not places.run("INSERT INTO wards (town_id, name) VALUES (999, 'Ghost');").ok, "town_id must be a real town"
    places.run("DELETE FROM towns WHERE name = 'Naivasha';").check()
    assert places.run("SELECT name FROM wards;").check().rows == [("Biashara",)]


def test_delete_kisumu(places, target):
    places.run_file(target / "4-delete_kisumu.sql").check()
    assert places.run("SELECT COUNT(*) FROM counties WHERE id = 6;").check().rows == [("0",)]
    assert places.run("SELECT COUNT(*) FROM towns WHERE county_id = 6;").check().rows == [("0",)]
    assert places.run("SELECT COUNT(*) FROM towns;").check().rows == [("11",)], "only Kisumu's two towns go"


def test_kata_who_points_here(places, target):
    places.run("CREATE TABLE offices (id INT PRIMARY KEY, county INT, FOREIGN KEY (county) REFERENCES counties (id));").check()
    result = places.run_file(target / "kata.sql").check()
    assert [c.lower() for c in result.columns] == ["table_name", "column_name"]
    assert result.rows == [("offices", "county"), ("towns", "county_id")]
