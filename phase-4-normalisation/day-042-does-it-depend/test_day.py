"""Day 42: Does It Depend?"""

import pytest

from coursekit import load_module

ROWS = [dict(zip(["student", "subject", "tutor", "room"], r)) for r in [
    ("Amani", "Maths", "Omondi", "R1"), ("Amani", "Physics", "Wairimu", "R2"),
    ("Baraka", "Maths", "Omondi", "R1"), ("Baraka", "Chemistry", "Kibet", "R3"),
    ("Cynthia", "Biology", "Achieng", "R3"),
]]


@pytest.fixture
def fd(target):
    return load_module(target / "fd_check.py")


def test_is_trivial(fd):
    assert fd.is_trivial(["A", "B"], ["A"])
    assert fd.is_trivial(["A"], ["A"])
    assert not fd.is_trivial(["A"], ["A", "B"])


def test_holds(fd):
    assert fd.holds(ROWS, ["subject"], ["tutor"])
    assert fd.holds(ROWS, ["tutor"], ["room"])
    assert not fd.holds(ROWS, ["room"], ["tutor"]), "R3 has Kibet and Achieng"
    assert fd.holds(ROWS, ["student", "subject"], ["tutor", "room"])
    assert not fd.holds(ROWS, ["student"], ["subject"])
    assert fd.holds([], ["a"], ["b"]), "nothing to contradict it"


def test_violations(fd):
    assert fd.violations(ROWS, ["room"], ["tutor"]) == [("R3",)]
    assert fd.violations(ROWS, ["student"], ["subject"]) == [("Amani",), ("Baraka",)]
    assert fd.violations(ROWS, ["subject"], ["tutor"]) == []


def test_plate_sacco_in_sql(mysql, day, target):
    mysql.load(day / "setup.sql")
    got = mysql.run_file(target / "0-plate_sacco_violations.sql").check()
    assert got.columns == ["plate", "saccos"] and got.rows == [("KDB 202B", "2")]
    mysql.run("UPDATE trips SET sacco = 'Pwani Express' WHERE sacco = 'Pwani Expres';").check()
    assert mysql.run_file(target / "0-plate_sacco_violations.sql").check().rows == []


def test_route_fare_in_sql(mysql, day, target):
    mysql.load(day / "setup.sql")
    got = mysql.run_file(target / "1-route_fare_holds.sql").check()
    assert got.columns == ["holds"] and got.rows == [("1",)]
    mysql.run("INSERT INTO trips (plate, sacco, route, driver, fare, trip_date) "
              "VALUES ('KDA 101A', 'Mwangaza Shuttle', '46', 'Otieno', 120, '2026-10-08');").check()
    assert mysql.run_file(target / "1-route_fare_holds.sql").check().rows == [("0",)]


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.AB_TO_A_IS_TRIVIAL, a.A_TO_AB_IS_TRIVIAL, a.IF_A_IS_A_KEY_THEN_A_DETERMINES_EVERY_ATTRIBUTE,
            a.SAMPLE_DATA_CAN_PROVE_AN_FD_HOLDS, a.SAMPLE_DATA_CAN_PROVE_AN_FD_FAILS,
            a.IF_A_TO_B_HOLDS_THEN_B_TO_A_HOLDS] == [True, False, True, False, True, False]
    assert (a.PLATE_DETERMINES_SACCO, a.DRIVER_DETERMINES_PLATE) == ("yes", "no")


def test_kata_find_them_all(fd):
    assert fd.holding_fds(ROWS, ["student", "subject", "tutor", "room"]) == [
        (("student", "room"), "subject"), (("student", "room"), "tutor"),
        (("subject",), "room"), (("subject",), "tutor"),
        (("tutor",), "room"), (("tutor",), "subject"),
    ]
