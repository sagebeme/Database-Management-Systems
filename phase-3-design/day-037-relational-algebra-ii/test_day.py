"""Day 37: Relational Algebra II."""

import pytest

from coursekit import load_module
from coursekit.relational import make, same

REGISTERED = make(["adm_no", "code"], [
    ("S0001", "COM101"), ("S0001", "COM102"), ("S0001", "MAT101"), ("S0001", "ENG110"),
    ("S0002", "COM101"), ("S0002", "MAT101"),
    ("S0003", "COM101"), ("S0003", "COM102"), ("S0003", "MAT101"), ("S0004", "ENG110"),
])
CORE = make(["code"], [("COM101",), ("COM102",), ("MAT101",)])
STUDENTS = make(["adm_no", "name"], [("S0001", "Achieng"), ("S0002", "Baraka"), ("S0003", "Chebet"),
                                     ("S0004", "Duncan"), ("S0005", "Esther")])


@pytest.fixture
def ra(target):
    return load_module(target / "algebra.py")


def test_natural_join(ra):
    got = ra.natural_join(STUDENTS, REGISTERED)
    assert got.heading == ("adm_no", "name", "code")
    assert len(got) == 10 and ("S0002", "Baraka", "MAT101") in got.rows
    assert len(ra.natural_join(make(["x"], [(1,), (2,)]), make(["y"], [(3,)]))) == 2, "nothing shared: a product"


def test_theta_join(ra):
    a = make(["n"], [(1,), (2,), (3,)])
    b = make(["m"], [(2,), (3,)])
    assert same(ra.theta_join(a, b, lambda t: t["n"] < t["m"]), make(["n", "m"], [(1, 2), (1, 3), (2, 3)]))
    with pytest.raises(ValueError):
        ra.theta_join(a, a, lambda t: True)


def test_left_outer_join(ra):
    got = ra.left_outer_join(STUDENTS, REGISTERED)
    assert len(got) == 11 and ("S0005", "Esther", None) in got.rows


def test_semi_join(ra):
    assert same(ra.semi_join(STUDENTS, make(["code", "adm_no"], [("ENG110", "S0001"), ("ENG110", "S0004")])),
                make(["adm_no", "name"], [("S0001", "Achieng"), ("S0004", "Duncan")]))


def test_divide(ra):
    assert same(ra.divide(REGISTERED, CORE), make(["adm_no"], [("S0001",), ("S0003",)]))
    assert same(ra.divide(REGISTERED, make(["code"], [("ENG110",)])), make(["adm_no"], [("S0001",), ("S0004",)]))
    assert same(ra.divide(REGISTERED, make(["code"], [])), make(["adm_no"], [("S0001",), ("S0002",), ("S0003",), ("S0004",)]))
    three = make(["a", "b", "c"], [(1, "x", 9), (1, "y", 9), (2, "x", 8), (2, "y", 7)])
    assert same(ra.divide(three, make(["b"], [("x",), ("y",)])), make(["a", "c"], [(1, 9)]))


@pytest.mark.parametrize("name", ["0-every_core_unit", "1-every_core_unit_by_counting"])
def test_division_in_sql(mysql, day, target, name):
    mysql.load(day / "setup.sql")
    assert mysql.run_file(target / f"{name}.sql").check().rows == [("Achieng",), ("Chebet",)]
    mysql.run("INSERT INTO units VALUES ('STA101', 'Statistics', TRUE); "
              "INSERT INTO registrations VALUES ('S0003', 'STA101');").check()
    assert mysql.run_file(target / f"{name}.sql").check().rows == [("Chebet",)], "a new core unit changes the answer"


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.MOST_TUPLES_IN_R_NATURAL_JOIN_S, a.MOST_TUPLES_IN_R_LEFT_JOIN_S,
            a.FEWEST_TUPLES_IN_R_LEFT_JOIN_S, a.DEGREE_OF_R_NATURAL_JOIN_S] == [6, 6, 6, 3]
    assert a.A_THETA_JOIN_IS_A_PRODUCT_FOLLOWED_BY == "select"
    assert a.EVERY_QUESTIONS_NEED == "division"
    assert a.DIVIDING_BY_AN_EMPTY_RELATION_RETURNS_EVERYTHING is True


def test_kata_division_the_hard_way(ra):
    assert same(ra.divide_with_basics(REGISTERED, CORE), make(["adm_no"], [("S0001",), ("S0003",)]))
    three = make(["a", "b", "c"], [(1, "x", 9), (1, "y", 9), (2, "x", 8), (2, "y", 7)])
    assert same(ra.divide_with_basics(three, make(["b"], [("x",), ("y",)])), make(["a", "c"], [(1, 9)]))
