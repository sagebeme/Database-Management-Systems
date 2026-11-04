"""Day 46: Splitting Without Losing."""

import pytest

from coursekit import load_module
from coursekit.fds import attrs, parse

ORIGINAL = "SELECT student, course, lecturer FROM enrolments ORDER BY student, course;"


@pytest.fixture
def ll(target):
    return load_module(target / "lossless.py")


@pytest.mark.parametrize("r1, r2, fds, ok", [
    ("AB", "CD", "A->B; C->D", False),
    ("AB", "ACD", "A->B; C->D", True),
    ("ABC", "CD", "A->B; C->D", True),
    ("AC", "BD", "A->B; C->D", False),
    ("AB", "BC", "B->C", True),
    ("AB", "BC", "C->B", False),
])
def test_binary_lossless(ll, r1, r2, fds, ok):
    assert ll.binary_lossless(attrs(r1), attrs(r2), parse(fds)) is ok


@pytest.mark.parametrize("schema, parts, fds, ok", [
    ("ABCDE", ["AD", "AB", "BE", "CDE", "AE"], "A->C; B->C; C->D; DE->C; CE->A", True),
    ("ABCD", ["AB", "BC", "CD"], "A->B; B->C; C->D; D->A", True),
    ("ABCD", ["AB", "CD"], "A->B; C->D", False),
    ("ABCDE", ["ABC", "CD", "DE"], "A->B; C->D", False),
    ("ABCDE", ["ABC", "CD", "CE"], "AB->C; C->D; C->E", True),
    ("ABCD", ["AB", "ACD"], "A->B", True),
])
def test_chase(ll, schema, parts, fds, ok):
    assert ll.chase(attrs(schema), [attrs(p) for p in parts], parse(fds)) is ok


def test_the_bad_split_makes_ghosts(mysql, day, target):
    mysql.load(day / "setup.sql")
    mysql.run_file(target / "0-split_badly.sql").check()
    assert mysql.run("SELECT COUNT(*) FROM student_lecturer;").check().rows == [("4",)]
    assert mysql.run("SELECT COUNT(*) FROM course_lecturer;").check().rows == [("3",)]
    got = mysql.run_file(target / "1-ghost_rows.sql").check()
    assert got.columns == ["student", "course", "lecturer"]
    assert got.rows == [("Achieng", "Compilers", "Dr Otieno")]


def test_ghost_query_on_other_data(mysql, day, target):
    mysql.load(day / "setup.sql")
    mysql.run("INSERT INTO enrolments VALUES ('Chebet', 'Security', 'Dr Wanjiku');").check()
    mysql.run_file(target / "0-split_badly.sql").check()
    assert mysql.run_file(target / "1-ghost_rows.sql").check().rows == [
        ("Achieng", "Compilers", "Dr Otieno"), ("Achieng", "Security", "Dr Wanjiku")]


def test_the_good_split_is_lossless(mysql, day, target):
    mysql.load(day / "setup.sql")
    mysql.run_file(target / "2-split_well.sql").check()
    got = mysql.run_file(target / "3-rejoin.sql").check()
    assert got.columns == ["student", "course", "lecturer"]
    assert got.rows == mysql.run(ORIGINAL).check().rows


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.AB_AND_CD, a.AB_AND_ACD, a.ABC_AND_CD, a.AC_AND_BD] == [False, True, True, False]
    assert (a.A_LOSSY_JOIN_LOSES_ROWS, a.A_LOSSY_JOIN_ADDS_ROWS_THAT_WERENT_THERE) == (False, True)


def test_kata_count_the_ghosts(ll):
    rows = [dict(zip(["student", "course", "lecturer"], r)) for r in [
        ("Achieng", "Databases", "Dr Otieno"), ("Achieng", "Networks", "Dr Wanjiku"),
        ("Baraka", "Databases", "Dr Otieno"), ("Baraka", "Compilers", "Dr Otieno"), ("Chebet", "Networks", "Dr Wanjiku")]]
    assert ll.spurious(rows, [{"student", "lecturer"}, {"course", "lecturer"}]) == [
        {"course": "Compilers", "lecturer": "Dr Otieno", "student": "Achieng"}]
    assert ll.spurious(rows, [{"student", "course"}, {"course", "lecturer"}]) == []
