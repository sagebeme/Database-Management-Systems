"""Day 54: Fans by Country."""

import pytest

# A new genre with one act, a tie at the top of Bongo Flava, and Nigeria drawing level with Tanzania.
SHAKE_UP = """INSERT INTO artists VALUES (21, 'Kalenjin Hills Beat', 'Kipsigis Pop', 'Kenya', 760000, 2016, NULL),
    (22, 'Arusha Mic', 'Bongo Flava', 'Tanzania', 980000, 2015, NULL);
UPDATE artists SET fans = 2240000 WHERE name = 'Ikeja Mainland';"""
QUERIES = ["1-rank_artists", "2-rank_within_genre", "3-top_two_per_genre", "4-share_of_country", "kata"]


@pytest.fixture
def music(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def run(db, folder, name):
    return db.run_file(folder / f"{name}.sql").check().rows


def test_fans_by_origin(music, target):
    assert run(music, target, "0-fans_by_origin") == [
        ("Kenya", "2920000"), ("Tanzania", "2760000"), ("Nigeria", "2390000"), ("DR Congo", "1740000"),
        ("Uganda", "1240000"), ("Rwanda", "300000")]


def test_rank_artists(music, target):
    rows = run(music, target, "1-rank_artists")
    assert rows[:3] == [("Lagos Lagoon Sound", "Nigeria", "1500000", "1"), ("Soukous ya Sika", "DR Congo", "1100000", "2"),
                        ("Dar Mtaa Crew", "Tanzania", "980000", "3")]
    assert [r[3] for r in rows[4:7]] == ["5", "5", "7"], "a tie shares a place and skips the next"
    assert rows[-1] == ("Nyota ya Pwani", "Kenya", "180000", "20")


def test_rank_within_genre(music, target):
    rows = run(music, target, "2-rank_within_genre")
    assert [r for r in rows if r[0] == "Gengetone"] == [
        ("Gengetone", "Mathare Vibes", "540000", "1"), ("Gengetone", "Ndovu Mtaani", "540000", "1"),
        ("Gengetone", "Buruburu Squad", "220000", "2")], "no gap after a tie"
    assert len(rows) == 20


def test_top_two_per_genre(music, target):
    rows = run(music, target, "3-top_two_per_genre")
    assert len(rows) == 14
    assert [r[1] for r in rows if r[0] == "Bongo Flava"] == ["Dar Mtaa Crew", "Kariakoo Kings"], \
        "exactly two, even with a tie for second"


def test_share_of_country(music, target):
    rows = run(music, target, "4-share_of_country")
    assert rows[:2] == [("Soukous ya Sika", "DR Congo", "1100000", "63.2"), ("Matonge Express", "DR Congo", "640000", "36.8")]
    assert ("Kigali Hills Choir", "Rwanda", "300000", "100.0") in rows


@pytest.mark.parametrize("name", QUERIES)
def test_on_other_data(music, day, target, name):
    music.run(SHAKE_UP).check()
    assert run(music, target, name) == run(music, day / "solution", name)


def test_kata_second_best_country(music, target):
    assert run(music, target, "kata") == [("Tanzania", "2760000")]
    music.run(SHAKE_UP).check()
    assert run(music, target, "kata") == [("Kenya", "3680000")], \
        "Nigeria and Tanzania tie for first, so Kenya is second (RANK would call it third)"
