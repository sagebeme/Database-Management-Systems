"""Day 28: Capstone, The Riverwood Report.

Each answer is compared with the reference answer on the same data, twice: on the data as given,
and after a shake-up that moves the answers around. Then a few answers are checked by hand.
"""

from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
NAMES = sorted(p.stem for p in (HERE / "solution").glob("*.sql"))

# A new comedy, a show that finds its genres, Jiko Wars losing its votes, a tie for best Crime
# show, and new watchlist requests.
SHAKE_UP = """
INSERT INTO tv_shows (id, title, first_aired, channel) VALUES (14, 'Boda Life', 2026, 'Jamii TV');
INSERT INTO tv_show_genres (show_id, genre_id)
    SELECT 14, id FROM tv_genres WHERE name IN ('Comedy', 'Family')
    UNION ALL SELECT 13, id FROM tv_genres WHERE name IN ('Drama', 'Romance')
    UNION ALL SELECT 10, id FROM tv_genres WHERE name = 'Documentary';
INSERT INTO tv_show_ratings (show_id, rate) VALUES
    (14, 10), (14, 10), (14, 10), (14, 9), (14, 9), (14, 9), (14, 9), (13, 9), (13, 10), (2, 1);
DELETE FROM tv_show_ratings WHERE show_id = 10;
INSERT INTO watchlist (viewer, show_id, requested_title) VALUES
    ('esther', NULL, 'Boda Boda Diaries'), ('faith', NULL, 'Boda Boda Diaries'),
    ('faith', NULL, 'Kina Mama'), ('akinyi', 12, NULL), ('baraka', 14, NULL);
"""


@pytest.fixture
def riverwood(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def answer(db, folder, name):
    return db.run_file(folder / f"{name}.sql").check()


def same_as_reference(db, day, target, name):
    got, want = answer(db, target, name), answer(db, day / "solution", name)
    assert got.columns == want.columns
    assert got.rows == want.rows


@pytest.mark.parametrize("name", NAMES)
def test_on_the_data(riverwood, day, target, name):
    same_as_reference(riverwood, day, target, name)


@pytest.mark.parametrize("name", NAMES)
def test_after_the_shake_up(riverwood, day, target, name):
    riverwood.run(SHAKE_UP).check()
    same_as_reference(riverwood, day, target, name)


def test_checked_by_hand(riverwood, target):
    def rows(name):
        return answer(riverwood, target, name).rows

    assert rows("0-show_list")[7] == ("Mwisho wa Reli", "NULL")
    assert rows("1-channel_lineup") == [("Bahari TV", "3"), ("Citi Lights", "3"), ("Jamii TV", "4"), ("Riverwood Plus", "3")]
    assert rows("2-genre_counts")[-1] == ("Documentary", "0")
    assert rows("3-comedies_by_rating")[0] == ("Shamba Boys", "61")
    assert rows("4-unrated") == [("Mwisho wa Reli",)]
    assert ("Matatu Kings",) in rows("5-not_drama") and ("Mama Pima",) not in rows("5-not_drama")
    assert rows("6-watchlist_counts")[0] == ("Nairobi Nights", "2")
    assert rows("7-wanted_titles") == [("Boda Boda Diaries", "1")]
    assert rows("8-akinyi_genres") == [("Crime",), ("Drama",), ("Mystery",), ("Romance",)]
    assert rows("9-channel_scores")[0] == ("Jamii TV", "7.52")
    assert ("Crime", "Kikosi Maalum", "40") in rows("10-best_in_genre")
    assert rows("11-watchlist_lines")[2] == ("chebet: Boda Boda Diaries, Shamba Boys, Shule Yetu",)
    assert rows("kata") == [("Shamba Boys", "Shule Yetu")]

    riverwood.run(SHAKE_UP).check()
    best = rows("10-best_in_genre")
    assert ("Crime", "Kikosi Maalum", "40") in best and ("Crime", "Nairobi Nights", "40") in best, "keep both on a tie"
    assert rows("4-unrated") == [("Jiko Wars",)]
    assert rows("7-wanted_titles")[0] == ("Boda Boda Diaries", "3")
    assert rows("kata") == [("Boda Life", "Shamba Boys"), ("Boda Life", "Shule Yetu"),
                            ("Mwisho wa Reli", "Pwani Love"), ("Shamba Boys", "Shule Yetu")]
