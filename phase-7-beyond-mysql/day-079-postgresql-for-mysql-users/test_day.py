"""Day 79: PostgreSQL for MySQL Users."""

import pytest

from coursekit import load_module


@pytest.fixture
def pg(postgres, day):
    postgres.load(day / "setup.sql")
    return postgres


def test_stages(pg, target):
    pg.run_file(target / "0-stages.sql").check()
    cols = pg.run("SELECT column_name, data_type, is_nullable, is_identity, identity_generation, column_default "
                  "FROM information_schema.columns WHERE table_name = 'stages' ORDER BY ordinal_position;").check().rows
    assert [c[0] for c in cols] == ["id", "name", "county"]
    assert cols[0][1:5] == ("integer", "NO", "YES", "ALWAYS"), "id: an INT identity column, GENERATED ALWAYS"
    assert cols[1][1:3] == ("text", "NO")
    assert cols[2][1:3] == ("text", "NO") and cols[2][5].startswith("'Nairobi'")
    pg.run("INSERT INTO stages (name) VALUES ('Kencom'), ('Odeon');").check()
    assert pg.run("SELECT id, name, county FROM stages ORDER BY id;").check().rows == [
        ("1", "Kencom", "Nairobi"), ("2", "Odeon", "Nairobi")]
    by_hand = pg.run("INSERT INTO stages (id, name) VALUES (10, 'Railways');")
    assert not by_hand.ok and "GENERATED ALWAYS" in by_hand.stderr
    assert not pg.run("INSERT INTO stages (name) VALUES ('Kencom');").ok, "name must be unique"
    assert not pg.run("INSERT INTO stages (name) VALUES (NULL);").ok


def test_reports_schema(pg, target):
    pg.run_file(target / "1-reports_schema.sql").check()
    got = pg.run("SELECT number, sacco, fare FROM reports.route_fares ORDER BY number;").check()
    assert got.columns == ["number", "sacco", "fare"]
    assert got.rows[:3] == [("105", "Jiji Shuttle", "100"), ("111", "Jiji Shuttle", "100"),
                            ("125", "Pwani Ride", "120")]
    assert len(got.rows) == 9
    assert not pg.run("SELECT * FROM route_fares;").ok, "the view lives in the reports schema, not public"
    pg.run("UPDATE routes SET fare = 75 WHERE number = '46';").check()
    assert ("46", "Mwendo Express", "75") in pg.run("SELECT * FROM reports.route_fares;").check().rows, \
        "a view, not a copy"


def test_returning(pg, target):
    got = pg.run_file(target / "2-returning.sql").check()
    assert got.columns == ["id", "name"]
    assert got.rows == [("5", "Mji Movers")]
    assert pg.run("SELECT count(*) FROM saccos WHERE name = 'Mji Movers';").check().rows == [("1",)]


def test_upsert(pg, target):
    route = "SELECT r.destination, s.name, r.fare FROM routes r JOIN saccos s ON s.id = r.sacco_id WHERE number = '44';"
    pg.run_file(target / "3-upsert.sql").check()
    assert pg.run(route).check().rows == [("Githurai", "Kilele Movers", "90")]
    pg.run("UPDATE routes SET destination = 'Githurai 45', fare = 50, sacco_id = 1 WHERE number = '44';").check()
    pg.run_file(target / "3-upsert.sql").check()
    assert pg.run(route).check().rows == [("Githurai", "Kilele Movers", "90")], "run again, it updates the route"
    assert pg.run("SELECT count(*) FROM routes;").check().rows == [("10",)]
    pg.run("UPDATE saccos SET name = 'Kilele Movers Ltd' WHERE name = 'Kilele Movers';"
           "INSERT INTO saccos (name) VALUES ('Kilele Movers');").check()
    pg.run_file(target / "3-upsert.sql").check()
    assert pg.run(route).check().rows == [("Githurai", "Kilele Movers", "90")], "look the sacco up by name"


def test_rongai(pg, target):
    got = pg.run_file(target / "4-rongai.sql").check()
    assert got.columns == ["number", "destination"]
    assert got.rows == [("125", "Ongata Rongai"), ("126", "Rongai via Lang'ata")]
    pg.run("INSERT INTO routes (number, destination, sacco_id, fare) VALUES ('24', 'RONGAI express', 2, 90);").check()
    assert ("24", "RONGAI express") in pg.run_file(target / "4-rongai.sql").check().rows


def test_answers(target, pg):
    a = load_module(target / "answers.py")
    tables = pg.run(a.LIST_TABLES).check().stdout
    assert "routes" in tables and "saccos" in tables, f"{a.LIST_TABLES!r} didn't list the tables"
    described = pg.run(a.DESCRIBE_ROUTES).check().stdout
    assert "destination" in described and "sacco_id" in described, f"{a.DESCRIBE_ROUTES!r} didn't describe routes"
    assert pg.database in pg.run(a.LIST_DATABASES).check().stdout
    assert a.USE_MATATU.split() in (["\\c", "matatu"], ["\\connect", "matatu"])
    assert a.QUIT in ("\\q", "\\quit")


def test_kata(pg, target, day):
    got = pg.run_file(target / "kata.sql").check()
    assert got.columns == ["sacco", "routes"]
    assert got.rows == [("Jiji Shuttle", "105, 111"), ("Kilele Movers", "237, 58"),
                        ("Mwendo Express", "19C, 33, 46"), ("Pwani Ride", "125, 126")]
    pg.run("INSERT INTO saccos (name) VALUES ('Bila Route');"
           "INSERT INTO routes (number, destination, sacco_id, fare) VALUES ('100', 'Kiambu', 2, 80);").check()
    got = pg.run_file(target / "kata.sql").check().rows
    assert got == pg.run_file(day / "solution" / "kata.sql").check().rows
    assert ("Bila Route", "NULL") in got
