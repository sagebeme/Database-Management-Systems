"""Day 38: Relational Calculus."""

import pytest

from coursekit import load_module

SHOWS = [
    {"title": "Mtaa wa Mapepe", "channel": "Jamii TV", "year": 2016},
    {"title": "Pwani Love", "channel": "Bahari TV", "year": 2021},
    {"title": "Mama Pima", "channel": "Bahari TV", "year": 2020},
    {"title": "Siri za Lamu", "channel": "Bahari TV", "year": 2022},
    {"title": "Nairobi Nights", "channel": "Citi Lights", "year": 2019},
    {"title": "Mwisho wa Reli", "channel": "Citi Lights", "year": 2025},
]
GENRES = [
    {"title": "Mtaa wa Mapepe", "genre": "Comedy"}, {"title": "Pwani Love", "genre": "Drama"},
    {"title": "Pwani Love", "genre": "Romance"}, {"title": "Mama Pima", "genre": "Drama"},
    {"title": "Siri za Lamu", "genre": "Mystery"}, {"title": "Nairobi Nights", "genre": "Drama"},
]
RATINGS = [
    {"title": "Mtaa wa Mapepe", "rate": 8}, {"title": "Mtaa wa Mapepe", "rate": 7},
    {"title": "Pwani Love", "rate": 9}, {"title": "Pwani Love", "rate": 3},
    {"title": "Siri za Lamu", "rate": 9}, {"title": "Nairobi Nights", "rate": 6}, {"title": "Mama Pima", "rate": 7},
]


@pytest.fixture
def calc(target):
    return load_module(target / "calculus.py")


def test_recent(calc):
    assert calc.recent(SHOWS) == {"Pwani Love", "Mama Pima", "Siri za Lamu", "Mwisho wa Reli"}


def test_has_drama(calc):
    assert calc.has_drama(SHOWS, GENRES) == {"Pwani Love", "Mama Pima", "Nairobi Nights"}


def test_no_genre(calc):
    assert calc.no_genre(SHOWS, GENRES) == {"Mwisho wa Reli"}
    assert calc.no_genre(SHOWS, []) == {s["title"] for s in SHOWS}


def test_never_below_seven_includes_the_unrated(calc):
    assert calc.never_below_seven(SHOWS, RATINGS) == {"Mtaa wa Mapepe", "Siri za Lamu", "Mama Pima", "Mwisho wa Reli"}


def test_never_below_seven_and_rated(calc):
    assert calc.never_below_seven_and_rated(SHOWS, RATINGS) == {"Mtaa wa Mapepe", "Siri za Lamu", "Mama Pima"}
    assert calc.never_below_seven_and_rated(SHOWS, []) == set()


def test_bahari_years_in_domain_calculus(calc):
    tuples = [(s["title"], s["channel"], s["year"]) for s in SHOWS]
    assert calc.bahari_years(tuples) == {2020, 2021, 2022}


def test_answers(target):
    a = load_module(target / "answers.py")
    assert a.THE_UNSAFE_ONE == "B"
    assert (a.TRC_VARIABLES_RANGE_OVER, a.DRC_VARIABLES_RANGE_OVER) == ("tuples", "domain values")
    assert [a.RELATIONAL_ALGEBRA_IS_PROCEDURAL, a.RELATIONAL_CALCULUS_IS_PROCEDURAL,
            a.SAFE_CALCULUS_AND_ALGEBRA_CAN_EXPRESS_THE_SAME_QUERIES] == [True, False, True]
    assert str(a.SQL_FOR_ALL).upper() == "NOT EXISTS"


def test_kata_every_without_division(calc):
    reg = [{"adm_no": a, "code": c} for a, c in [
        ("S1", "COM101"), ("S1", "COM102"), ("S1", "MAT101"), ("S2", "COM101"), ("S3", "COM101"),
        ("S3", "COM102"), ("S3", "MAT101"), ("S3", "ENG110"), ("S4", "ENG110")]]
    core = [{"code": c} for c in ("COM101", "COM102", "MAT101")]
    assert calc.every_core_unit(reg, core) == {"S1", "S3"}
    assert calc.every_core_unit(reg, []) == {"S1", "S2", "S3", "S4"}
