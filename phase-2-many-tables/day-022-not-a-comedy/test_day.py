"""Day 22: Not a Comedy. Each test also changes the data, so typed-in answers fail."""

import pytest

COMEDY = "(SELECT id FROM tv_genres WHERE name = 'Comedy')"


@pytest.fixture
def riverwood(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def titles(db, path):
    result = db.run_file(path).check()
    assert len(result.columns) == 1, f"one column, got {result.columns}"
    return result.column(0)


def test_not_a_comedy(riverwood, target):
    path = target / "0-not_a_comedy.sql"
    got = titles(riverwood, path)
    assert got == ["Fundi Hacker", "Jiko Wars", "Kesho Kutwa", "Kikosi Maalum", "Mama Pima",
                   "Mwisho wa Reli", "Nairobi Nights", "Pwani Love", "Siri za Lamu"]
    riverwood.run(f"INSERT INTO tv_show_genres SELECT 13, {COMEDY};").check()
    assert "Mwisho wa Reli" not in titles(riverwood, path)


def test_not_my_genres(riverwood, target):
    path = target / "1-not_my_genres.sql"
    got = titles(riverwood, path)
    assert got == ["Action", "Comedy", "Documentary", "Drama", "Family", "Mystery", "Reality", "Romance", "Sci-Fi"]
    riverwood.run(f"INSERT INTO tv_show_genres SELECT 7, {COMEDY};").check()
    assert "Comedy" not in titles(riverwood, path)


def test_shows_without_genres(riverwood, target):
    path = target / "2-shows_without_genres.sql"
    assert titles(riverwood, path) == ["Mwisho wa Reli"]
    riverwood.run("DELETE FROM tv_show_genres WHERE show_id = 10;").check()
    assert titles(riverwood, path) == ["Jiko Wars", "Mwisho wa Reli"]


def test_unused_genres(riverwood, target):
    path = target / "3-unused_genres.sql"
    assert titles(riverwood, path) == ["Documentary"]
    riverwood.run("INSERT INTO tv_genres (name) VALUES ('Horror');").check()
    assert titles(riverwood, path) == ["Documentary", "Horror"]


def test_nobody_saved_despite_the_null(riverwood, target):
    path = target / "4-nobody_saved.sql"
    got = titles(riverwood, path)
    assert got, "no rows: NOT IN met the NULL in watchlist.show_id. Try NOT EXISTS."
    assert got == ["Jiko Wars", "Mama Pima", "Matatu Kings", "Mtaa wa Mapepe", "Mwisho wa Reli", "Pwani Love"]
    riverwood.run("INSERT INTO watchlist (viewer, show_id) VALUES ('esther', 6);").check()
    assert "Mama Pima" not in titles(riverwood, path)


def test_kata_channels_without_laughs(riverwood, target):
    path = target / "kata.sql"
    assert titles(riverwood, path) == ["Bahari TV", "Citi Lights", "Riverwood Plus"]
    riverwood.run(f"INSERT INTO tv_show_genres SELECT 3, {COMEDY};").check()
    assert titles(riverwood, path) == ["Citi Lights", "Riverwood Plus"]
