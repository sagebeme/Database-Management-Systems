"""Day 23: Ratings. Each answer is checked on the data, then again after new votes come in,
against the same question asked by a reference query."""

import pytest

REFERENCE = {
    "0-rating_shows": (["title", "rating"], """
        SELECT s.title, SUM(r.rate) FROM tv_shows s JOIN tv_show_ratings r ON r.show_id = s.id
        GROUP BY s.id, s.title ORDER BY 2 DESC, 1"""),
    "1-rating_genres": (["name", "rating"], """
        SELECT g.name, SUM(r.rate) FROM tv_genres g JOIN tv_show_genres sg ON sg.genre_id = g.id
        JOIN tv_show_ratings r ON r.show_id = sg.show_id GROUP BY g.id, g.name ORDER BY 2 DESC, 1"""),
    "2-fair_averages": (["title", "average", "votes"], """
        SELECT s.title, ROUND(AVG(r.rate), 2), COUNT(*) FROM tv_shows s JOIN tv_show_ratings r ON r.show_id = s.id
        GROUP BY s.id, s.title HAVING COUNT(*) >= 5 ORDER BY AVG(r.rate) DESC, 1"""),
    "3-votes_per_show": (["title", "votes"], """
        SELECT s.title, (SELECT COUNT(*) FROM tv_show_ratings r WHERE r.show_id = s.id) AS v
        FROM tv_shows s ORDER BY v DESC, 1"""),
    "4-above_average_genres": (["genre", "average"], """
        SELECT g.name, ROUND(AVG(r.rate), 2) FROM tv_genres g JOIN tv_show_genres sg ON sg.genre_id = g.id
        JOIN tv_show_ratings r ON r.show_id = sg.show_id GROUP BY g.id, g.name
        HAVING AVG(r.rate) > (SELECT AVG(rate) FROM tv_show_ratings) ORDER BY AVG(r.rate) DESC, 1"""),
    "kata": (["title", "rating"], """
        SELECT s.title, SUM(r.rate) FROM tv_shows s JOIN tv_show_ratings r ON r.show_id = s.id
        GROUP BY s.id, s.title
        HAVING SUM(r.rate) > (SELECT SUM(rate) / COUNT(DISTINCT show_id) FROM tv_show_ratings)
        ORDER BY 2 DESC, 1"""),
}

# New votes that reshuffle the tables: Mwisho wa Reli gets its first five, Jiko Wars a fifth.
NEW_VOTES = """INSERT INTO tv_show_ratings (show_id, rate) VALUES
    (13, 10), (13, 10), (13, 9), (13, 10), (13, 9), (10, 10), (11, 1), (11, 2);"""


@pytest.fixture
def riverwood(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def check(db, target, name):
    columns, reference = REFERENCE[name]
    got = db.run_file(target / f"{name}.sql").check()
    assert got.columns == columns
    assert got.rows == db.run(reference + ";").check().rows
    return got.rows


@pytest.mark.parametrize("name", list(REFERENCE))
def test_on_the_data(riverwood, target, name):
    check(riverwood, target, name)


@pytest.mark.parametrize("name", list(REFERENCE))
def test_after_new_votes(riverwood, target, name):
    riverwood.run(NEW_VOTES).check()
    check(riverwood, target, name)


def test_known_answers(riverwood, target):
    assert check(riverwood, target, "0-rating_shows")[:3] == [
        ("Shamba Boys", "61"), ("Shule Yetu", "54"), ("Siri za Lamu", "54")]
    assert check(riverwood, target, "1-rating_genres")[0] == ("Comedy", "188")
    fair = check(riverwood, target, "2-fair_averages")
    assert "Jiko Wars" not in [row[0] for row in fair], "Jiko Wars has only 4 votes"
    assert fair[0] == ("Shule Yetu", "9.00", "6")
    assert check(riverwood, target, "3-votes_per_show")[-1] == ("Mwisho wa Reli", "0")
    assert [g for g, _ in check(riverwood, target, "4-above_average_genres")] == [
        "Mystery", "Family", "Sci-Fi", "Thriller", "Comedy", "Crime"]
    assert len(check(riverwood, target, "kata")) == 5
