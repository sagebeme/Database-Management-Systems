"""Day 31: Rules the Database Enforces. Each table is tested on its own, with the reference
answers for the tables it depends on."""

import pytest

from coursekit import load_module


@pytest.fixture
def db(mysql, day):
    def build(*names, target=None):
        for name in names:
            folder = target if target is not None and name == names[-1] else day / "solution"
            mysql.run_file(folder / name).check()
        return mysql
    return build


def refused(db, sql):
    return not db.run(sql).ok


def test_riders(db, target):
    m = db("0-riders.sql", target=target)
    m.run("INSERT INTO riders (name, licence_no, age) VALUES ('Kevin Ouma', 'DL0000001', 18), "
          "('Mary Atieno', 'DL0000002', 70);").check()
    assert refused(m, "INSERT INTO riders (name, licence_no, age) VALUES ('Too Young', 'DL0000003', 17);")
    assert refused(m, "INSERT INTO riders (name, licence_no, age) VALUES ('Too Old', 'DL0000004', 71);")
    assert refused(m, "INSERT INTO riders (name, licence_no, age) VALUES ('Copy', 'DL0000001', 30);")
    assert refused(m, "INSERT INTO riders (name, licence_no, age) VALUES (NULL, 'DL0000005', 30);")
    assert refused(m, "INSERT INTO riders (name, licence_no) VALUES ('No Age', 'DL0000006');")
    m.run_file(target / "0-riders.sql").check()


def test_bikes(db, target):
    m = db("0-riders.sql", "1-bikes.sql", target=target)
    m.run("INSERT INTO riders (id, name, licence_no, age) VALUES (1, 'Kevin Ouma', 'DL0000001', 25);").check()
    m.run("INSERT INTO bikes VALUES ('KMEA 001A', 1, 150), ('KMEB 002B', NULL, 125);").check()
    assert refused(m, "INSERT INTO bikes VALUES ('KMEC 003C', 99, 150);"), "rider 99 doesn't exist"
    assert refused(m, "INSERT INTO bikes VALUES ('KMED 004D', 1, 30);"), "30cc is out of range"
    m.run("UPDATE riders SET id = 100 WHERE id = 1;").check()
    assert m.run("SELECT rider_id FROM bikes WHERE plate = 'KMEA 001A';").check().rows == [("100",)], "ON UPDATE CASCADE"
    m.run("DELETE FROM riders WHERE id = 100;").check()
    assert m.run("SELECT rider_id FROM bikes WHERE plate = 'KMEA 001A';").check().rows == [("NULL",)], "ON DELETE SET NULL"


def test_trips(db, target):
    m = db("0-riders.sql", "1-bikes.sql", "2-trips.sql", target=target)
    m.run("INSERT INTO bikes VALUES ('KMEA 001A', NULL, 150);").check()
    m.run("INSERT INTO trips (plate, fare, started_at, ended_at) VALUES "
          "('KMEA 001A', 100, '2026-11-01 07:00', '2026-11-01 07:20'), ('KMEA 001A', 50, '2026-11-01 08:00', NULL);").check()
    assert refused(m, "INSERT INTO trips (plate, fare, started_at) VALUES ('KMEA 001A', 0, '2026-11-01 09:00');")
    assert refused(m, "INSERT INTO trips (plate, fare, started_at) VALUES ('NOPE', 80, '2026-11-01 09:00');")
    assert refused(m, "INSERT INTO trips (plate, fare, started_at, ended_at) "
                      "VALUES ('KMEA 001A', 80, '2026-11-01 09:00', '2026-11-01 08:59');"), "ends before it starts"
    m.run("UPDATE bikes SET plate = 'KMEZ 999Z' WHERE plate = 'KMEA 001A';").check()
    assert m.run("SELECT COUNT(*) FROM trips WHERE plate = 'KMEZ 999Z';").check().rows == [("2",)]
    m.run("DELETE FROM bikes WHERE plate = 'KMEZ 999Z';").check()
    assert m.run("SELECT COUNT(*) FROM trips;").check().rows == [("0",)], "ON DELETE CASCADE"


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.RIDER_AGED_TWELVE, a.RIDER_WITH_NULL_ID, a.TWO_RIDERS_SAME_LICENCE,
            a.BIKE_OF_RIDER_99_WHO_DOES_NOT_EXIST, a.TRIP_WITH_FARE_MINUS_50,
            a.DELETING_A_RIDER_WHOSE_BIKES_STILL_POINT_AT_THEM, a.ENGINE_CC_OF_TEXT_FAST] == [
        "domain", "entity", "key", "referential", "domain", "referential", "domain"]


def test_kata_name_the_rule(db, target):
    m = db("0-riders.sql", "kata.sql", target=target)
    names = m.run("SELECT constraint_name FROM information_schema.check_constraints "
                  "WHERE constraint_schema = DATABASE();").check().column(0)
    assert "phone_format" in names
    m.run("INSERT INTO riders (name, licence_no, age, phone) VALUES ('A', 'DL1', 30, '254712345678'), "
          "('B', 'DL2', 30, '254112345678'), ('C', 'DL3', 30, NULL);").check()
    for bad in ("0712345678", "254812345678", "25471234567X", "+25471234567"):
        assert refused(m, f"INSERT INTO riders (name, licence_no, age, phone) VALUES ('X', 'DL9', 30, '{bad}');"), bad
