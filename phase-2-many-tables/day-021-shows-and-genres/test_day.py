"""Day 21: Riverwood: Shows and Genres."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "datasets"))
from make_riverwood import JUNCTION_DDL  # noqa: E402


@pytest.fixture
def shows(mysql, day):
    """Shows and genres only: the junction table is yours to make."""
    mysql.load(day / "setup.sql")
    return mysql


@pytest.fixture
def riverwood(shows, day):
    """The whole database, with a correct junction table, for the query tasks."""
    shows.run(JUNCTION_DDL).check()
    shows.load(day / "links.sql")
    return shows


def got(db, path, columns):
    result = db.run_file(path).check()
    assert result.columns == columns
    return result.rows


def test_junction_table(shows, day, target):
    shows.run_file(target / "0-junction_table.sql").check()
    assert shows.run_file(target / "0-junction_table.sql").ok, "IF NOT EXISTS"
    shows.load(day / "links.sql")
    assert shows.run("SELECT COUNT(*) FROM tv_show_genres;").check().rows == [("22",)]
    assert not shows.run("INSERT INTO tv_show_genres VALUES (1, 2);").ok, "each pair at most once"
    assert not shows.run("INSERT INTO tv_show_genres VALUES (99, 2);").ok, "show_id must be a real show"
    assert not shows.run("INSERT INTO tv_show_genres VALUES (1, 99);").ok, "genre_id must be a real genre"
    assert not shows.run("INSERT INTO tv_show_genres VALUES (NULL, 2);").ok, "show_id is required"


def test_genres_of_nairobi_nights(riverwood, target):
    assert got(riverwood, target / "1-genres_of_nairobi_nights.sql", ["name"]) == [("Crime",), ("Drama",)]


def test_comedies(riverwood, target):
    assert got(riverwood, target / "2-comedies.sql", ["title"]) == [
        ("Matatu Kings",), ("Mtaa wa Mapepe",), ("Shamba Boys",), ("Shule Yetu",),
    ]


def test_shows_per_genre(riverwood, target):
    rows = got(riverwood, target / "3-shows_per_genre.sql", ["genre", "number_of_shows"])
    assert rows[:3] == [("Comedy", "4"), ("Drama", "4"), ("Crime", "3")]
    assert "Documentary" not in [g for g, _ in rows], "only genres that have shows"
    assert len(rows) == 10


def test_every_show_and_genre(riverwood, target):
    rows = got(riverwood, target / "4-every_show_and_genre.sql", ["title", "genre"])
    assert len(rows) == 23, "22 show-genre pairs, plus Mwisho wa Reli with no genre"
    assert ("Mwisho wa Reli", "NULL") in rows
    assert rows[:2] == [("Fundi Hacker", "Crime"), ("Fundi Hacker", "Thriller")]


def test_kata_romance_and_drama(riverwood, target):
    assert got(riverwood, target / "kata.sql", ["title"]) == [("Pwani Love",), ("Siri za Lamu",)]
