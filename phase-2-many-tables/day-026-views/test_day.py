"""Day 26: Views. A view must be a real view (not a copied table), so each test changes the
base tables afterwards and checks that the view changed with them."""

import pytest

SHOW_SCORES = """CREATE VIEW show_scores AS
SELECT s.id AS show_id, s.title, COUNT(r.show_id) AS votes, ROUND(AVG(r.rate), 2) AS average
FROM tv_shows s LEFT JOIN tv_show_ratings r ON r.show_id = s.id GROUP BY s.id, s.title;"""
CATALOGUE = """CREATE VIEW catalogue AS
SELECT s.title, s.channel, s.first_aired, GROUP_CONCAT(g.name ORDER BY g.name SEPARATOR ', ') AS genres
FROM tv_shows s LEFT JOIN tv_show_genres sg ON sg.show_id = s.id LEFT JOIN tv_genres g ON g.id = sg.genre_id
GROUP BY s.id, s.title, s.channel, s.first_aired;"""


@pytest.fixture
def riverwood(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def is_view(db, name):
    rows = db.run(f"SELECT table_type FROM information_schema.tables "
                  f"WHERE table_schema = DATABASE() AND table_name = '{name}';").check().rows
    return rows == [("VIEW",)]


def select(db, sql):
    return db.run(sql).check()


def test_catalogue_view(riverwood, target):
    riverwood.run_file(target / "0-catalogue_view.sql").check()
    assert is_view(riverwood, "catalogue"), "make a VIEW, not a table"
    got = select(riverwood, "SELECT * FROM catalogue ORDER BY title;")
    assert got.columns == ["title", "channel", "first_aired", "genres"]
    assert len(got.rows) == 13
    rows = {r[0]: r for r in got.rows}
    assert rows["Siri za Lamu"] == ("Siri za Lamu", "Bahari TV", "2022", "Drama, Mystery, Romance")
    assert rows["Mwisho wa Reli"][3] == "NULL"
    riverwood.run("INSERT INTO tv_show_genres VALUES (13, 5);").check()
    assert select(riverwood, "SELECT genres FROM catalogue WHERE title = 'Mwisho wa Reli';").rows == [("Drama",)]


def test_show_scores_view(riverwood, target):
    riverwood.run_file(target / "1-show_scores_view.sql").check()
    assert is_view(riverwood, "show_scores")
    got = select(riverwood, "SELECT * FROM show_scores ORDER BY show_id;")
    assert got.columns == ["show_id", "title", "votes", "average"]
    assert got.rows[4] == ("5", "Shamba Boys", "7", "8.71")
    assert got.rows[12] == ("13", "Mwisho wa Reli", "0", "NULL")
    riverwood.run("INSERT INTO tv_show_ratings VALUES (13, 8), (13, 9);").check()
    assert select(riverwood, "SELECT votes, average FROM show_scores WHERE show_id = 13;").rows == [("2", "8.50")]


def test_top_three(riverwood, target):
    riverwood.run(SHOW_SCORES).check()
    sql = (target / "2-top_three.sql").read_text()
    assert "show_scores" in sql, "query the view"
    got = riverwood.run(sql).check()
    assert got.columns == ["title", "average"]
    assert got.rows == [("Shule Yetu", "9.00"), ("Siri za Lamu", "9.00"), ("Shamba Boys", "8.71")]
    riverwood.run("INSERT INTO tv_show_ratings VALUES " + ", ".join(["(13, 10)"] * 5) + ";").check()
    assert riverwood.run(sql).check().rows[0] == ("Mwisho wa Reli", "10.00")


def test_catalogue_with_scores(riverwood, target):
    riverwood.run(SHOW_SCORES + CATALOGUE).check()
    riverwood.run_file(target / "3-catalogue_with_scores.sql").check()
    riverwood.run_file(target / "3-catalogue_with_scores.sql").check()  # replace works twice
    assert is_view(riverwood, "catalogue")
    got = select(riverwood, "SELECT * FROM catalogue ORDER BY title;")
    assert got.columns == ["title", "channel", "first_aired", "genres", "average"]
    assert len(got.rows) == 13, "every show, rated or not"
    rows = {r[0]: r for r in got.rows}
    assert rows["Siri za Lamu"][3:] == ("Drama, Mystery, Romance", "9.00")
    assert rows["Mwisho wa Reli"][3:] == ("NULL", "NULL")


def test_jamii_desk(riverwood, target):
    riverwood.run_file(target / "4-jamii_desk.sql").check()
    assert is_view(riverwood, "jamii_shows")
    got = select(riverwood, "SELECT title FROM jamii_shows ORDER BY title;")
    assert got.column(0) == ["Matatu Kings", "Mtaa wa Mapepe", "Shamba Boys", "Shule Yetu"]
    riverwood.run("INSERT INTO jamii_shows (title, first_aired, channel) VALUES ('Boda Life', 2026, 'Jamii TV');").check()
    assert select(riverwood, "SELECT channel FROM tv_shows WHERE title = 'Boda Life';").rows == [("Jamii TV",)]
    assert not riverwood.run("INSERT INTO jamii_shows (title, first_aired, channel) "
                             "VALUES ('Sneaky', 2026, 'Bahari TV');").ok, "WITH CHECK OPTION"
    assert not riverwood.run("UPDATE jamii_shows SET channel = 'Citi Lights' WHERE title = 'Shule Yetu';").ok
    riverwood.run("UPDATE jamii_shows SET first_aired = 2013 WHERE title = 'Shule Yetu';").check()


def test_kata_genre_board(riverwood, target):
    riverwood.run_file(target / "kata.sql").check()
    assert is_view(riverwood, "genre_board")
    got = select(riverwood, "SELECT * FROM genre_board ORDER BY genre;")
    assert got.columns == ["genre", "shows", "votes", "average"]
    rows = {r[0]: r[1:] for r in got.rows}
    assert len(rows) == 11
    assert rows["Comedy"] == ("4", "25", "7.52")
    assert rows["Documentary"] == ("0", "0", "NULL")
    assert rows["Drama"][0] == "4", "count shows once each, not once per vote"
    riverwood.run("INSERT INTO tv_show_genres VALUES (13, 4); INSERT INTO tv_show_ratings VALUES (13, 6);").check()
    assert select(riverwood, "SELECT shows, votes, average FROM genre_board WHERE genre = 'Documentary';").rows \
        == [("1", "1", "6.00")]
