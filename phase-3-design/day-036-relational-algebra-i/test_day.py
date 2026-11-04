"""Day 36: Relational Algebra I."""

import pytest

from coursekit import load_module
from coursekit.relational import make, same

SHOWS = make(["title", "channel", "year"], [
    ("Mtaa wa Mapepe", "Jamii TV", 2016), ("Nairobi Nights", "Citi Lights", 2019),
    ("Pwani Love", "Bahari TV", 2021), ("Kikosi Maalum", "Citi Lights", 2018),
    ("Shamba Boys", "Jamii TV", 2015), ("Mama Pima", "Bahari TV", 2020),
    ("Siri za Lamu", "Bahari TV", 2022), ("Mwisho wa Reli", "Citi Lights", 2025),
])
GENRES = make(["title", "genre"], [
    ("Mtaa wa Mapepe", "Comedy"), ("Nairobi Nights", "Crime"), ("Nairobi Nights", "Drama"),
    ("Pwani Love", "Drama"), ("Pwani Love", "Romance"), ("Kikosi Maalum", "Action"),
    ("Shamba Boys", "Comedy"), ("Shamba Boys", "Family"), ("Mama Pima", "Drama"), ("Siri za Lamu", "Mystery"),
])


def titles(*names):
    return make(["title"], [(n,) for n in names])


@pytest.fixture
def ra(target):
    return load_module(target / "algebra.py")


def test_select(ra):
    got = ra.select(SHOWS, lambda t: t["year"] >= 2021)
    assert got.heading == SHOWS.heading
    assert {row[0] for row in got.rows} == {"Pwani Love", "Siri za Lamu", "Mwisho wa Reli"}
    assert len(ra.select(SHOWS, lambda t: False)) == 0


def test_project_removes_duplicates(ra):
    got = ra.project(SHOWS, ["channel"])
    assert got.heading == ("channel",) and len(got) == 3
    assert ra.project(SHOWS, ["year", "title"]).heading == ("year", "title")
    with pytest.raises(ValueError):
        ra.project(SHOWS, ["rating"])


def test_rename(ra):
    got = ra.rename(SHOWS, {"title": "name"})
    assert got.heading == ("name", "channel", "year") and got.rows == SHOWS.rows


def test_union_and_difference(ra):
    a = make(["title", "year"], [("Pwani Love", 2021), ("Mama Pima", 2020)])
    b = make(["year", "title"], [(2020, "Mama Pima"), (2015, "Shamba Boys")])
    assert same(ra.union(a, b), make(["title", "year"], [("Pwani Love", 2021), ("Mama Pima", 2020), ("Shamba Boys", 2015)]))
    assert ra.union(a, b).heading == ("title", "year")
    assert same(ra.difference(a, b), make(["title", "year"], [("Pwani Love", 2021)]))
    with pytest.raises(ValueError):
        ra.union(a, titles("x"))
    with pytest.raises(ValueError):
        ra.difference(a, titles("x"))


def test_product(ra):
    a = make(["x"], [(1,), (2,)])
    b = make(["y", "z"], [("p", 0), ("q", 0), ("r", 1)])
    got = ra.product(a, b)
    assert got.heading == ("x", "y", "z") and len(got) == 6 and (2, "r", 1) in got.rows
    with pytest.raises(ValueError):
        ra.product(a, make(["x"], [(3,)]))


def test_queries(ra):
    assert same(ra.titles_on_bahari(SHOWS), titles("Pwani Love", "Mama Pima", "Siri za Lamu"))
    assert same(ra.comedy_or_drama(GENRES),
                titles("Mtaa wa Mapepe", "Shamba Boys", "Nairobi Nights", "Pwani Love", "Mama Pima"))
    assert same(ra.without_genre(SHOWS, GENRES), titles("Mwisho wa Reli"))
    assert same(ra.same_channel_pairs(SHOWS), make(["first", "second"], [
        ("Mtaa wa Mapepe", "Shamba Boys"), ("Kikosi Maalum", "Nairobi Nights"), ("Kikosi Maalum", "Mwisho wa Reli"),
        ("Mwisho wa Reli", "Nairobi Nights"), ("Mama Pima", "Pwani Love"), ("Mama Pima", "Siri za Lamu"),
        ("Pwani Love", "Siri za Lamu"),
    ]))


def test_queries_on_other_data(ra):
    shows = make(["title", "channel", "year"], [("A", "Bahari TV", 2000), ("B", "Bahari TV", 2001), ("C", "X", 1)])
    genres = make(["title", "genre"], [("A", "Drama"), ("C", "Comedy")])
    assert same(ra.titles_on_bahari(shows), titles("A", "B"))
    assert same(ra.comedy_or_drama(genres), titles("A", "C"))
    assert same(ra.without_genre(shows, genres), titles("B"))
    assert same(ra.same_channel_pairs(shows), make(["first", "second"], [("A", "B")]))


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.MOST_TUPLES_IN_R_UNION_S, a.FEWEST_TUPLES_IN_R_UNION_S, a.MOST_TUPLES_IN_R_MINUS_S,
            a.FEWEST_TUPLES_IN_R_MINUS_S, a.TUPLES_IN_R_TIMES_T, a.DEGREE_OF_R_TIMES_T,
            a.MOST_TUPLES_IN_A_SELECTION_OF_R, a.FEWEST_TUPLES_IN_A_PROJECTION_OF_R] == [16, 10, 10, 4, 40, 5, 10, 1]
    assert [a.INTERSECTION_IS_ONE_OF_THE_BASIC_SIX, a.SELECT_THEN_SELECT_EQUALS_ONE_SELECT_WITH_AND,
            a.UNION_IS_COMMUTATIVE, a.DIFFERENCE_IS_COMMUTATIVE] == [False, True, True, False]


def test_kata_only_minus(ra, target):
    a = make(["t"], [(1,), (2,), (3,)])
    b = make(["t"], [(2,), (3,), (4,)])
    assert same(ra.intersection(a, b), make(["t"], [(2,), (3,)]))
    source = (target / "algebra.py").read_text().split("def intersection", 1)[1]
    assert "&" not in source and " in " not in source, "only difference(), no Python set tricks"
