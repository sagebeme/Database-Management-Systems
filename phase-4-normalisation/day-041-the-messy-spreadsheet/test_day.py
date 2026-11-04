"""Day 41: The Messy Spreadsheet."""

import pytest

from coursekit import load_module

FLAT = "SELECT * FROM registrations_flat ORDER BY student, subject;"


@pytest.fixture
def flat(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


@pytest.fixture
def split(flat, day):
    flat.run_file(day / "solution" / "2-split.sql").check()
    return flat


def test_rows_for_one_fact(flat, target):
    got = flat.run_file(target / "0-rows_for_one_fact.sql").check()
    assert got.columns == ["rows"] and got.rows == [("3",)]
    flat.run("INSERT INTO registrations_flat VALUES ('Daudi Mwita', '254744000004', 'Maths', 3000, 'Mr Omondi', 'R1');").check()
    assert flat.run_file(target / "0-rows_for_one_fact.sql").check().rows == [("4",)]


def test_omondi_moves(flat, target):
    flat.run_file(target / "1-omondi_moves.sql").check()
    rooms = flat.run("SELECT DISTINCT tutor_room FROM registrations_flat WHERE tutor = 'Mr Omondi';").check().rows
    assert rooms == [("R5",)]
    assert flat.run("SELECT COUNT(*) FROM registrations_flat WHERE tutor_room = 'R5';").check().rows == [("3",)]


def test_split(flat, target):
    flat.run_file(target / "2-split.sql").check()
    counts = flat.run("SELECT (SELECT COUNT(*) FROM tutors), (SELECT COUNT(*) FROM subjects), "
                      "(SELECT COUNT(*) FROM students), (SELECT COUNT(*) FROM registrations);").check().rows
    assert counts == [("4", "4", "4", "7")], "each fact once: 4 tutors, 4 subjects, 4 students, 7 registrations"
    assert not flat.run("INSERT INTO subjects VALUES ('Art', 1000, 'Nobody');").ok, "a subject's tutor must exist"
    assert not flat.run("INSERT INTO registrations VALUES ('Nobody', 'Maths');").ok, "a registration's student must exist"
    assert not flat.run("INSERT INTO students VALUES ('Copy Cat', '254711000001');").ok, "phones are unique"
    assert not flat.run("INSERT INTO tutors VALUES ('Mr Omondi', 'R9');").ok, "one row per tutor"


def test_add_geography(split, target):
    split.run_file(target / "3-add_geography.sql").check()
    assert split.run("SELECT s.fee, t.room FROM subjects s JOIN tutors t ON t.name = s.tutor "
                     "WHERE s.name = 'Geography';").check().rows == [("2800", "R6")]
    assert split.run("SELECT COUNT(*) FROM registrations WHERE subject = 'Geography';").check().rows == [("0",)]


def test_rebuild_is_lossless(split, target):
    got = split.run_file(target / "4-rebuild.sql").check()
    original = split.run(FLAT).check()
    assert got.columns == original.columns
    assert got.rows == original.rows, "joining the parts must give back exactly the spreadsheet"
    split.run("UPDATE tutors SET room = 'R5' WHERE name = 'Mr Omondi';").check()
    assert sum(r[5] == "R5" for r in split.run_file(target / "4-rebuild.sql").check().rows) == 3, \
        "one change in tutors shows in all three rows"


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.OMONDI_CHANGES_ROOM_AND_ONE_ROW_IS_MISSED, a.CANNOT_RECORD_GEOGRAPHY_UNTIL_SOMEONE_REGISTERS,
            a.CYNTHIA_LEAVES_AND_THE_BIOLOGY_FEE_IS_FORGOTTEN, a.A_NEW_TUTOR_CANNOT_BE_ADDED_WITHOUT_A_STUDENT,
            a.MATHS_FEE_RISE_MUST_CHANGE_THREE_ROWS] == ["update", "insert", "delete", "insert", "update"]


def test_kata_fee_rise(split, target):
    split.run_file(target / "kata.sql").check()
    fees = dict(split.run("SELECT name, fee FROM subjects;").check().rows)
    assert fees == {"Maths": "3000", "Physics": "3850", "Chemistry": "3500", "Biology": "3200"}
