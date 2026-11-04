"""Day 6: KCSE Top Ten. Order matters today, so results are compared row by row, in order."""

import pytest


@pytest.fixture
def results(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def same(db, path, reference):
    got = db.run_file(path).check()
    want = db.run(reference).check()
    assert got.columns == want.columns
    assert got.rows == want.rows
    return got


def test_everyone_best_first(results, target):
    got = same(results, target / "0-top_score.sql", "SELECT name, points FROM results ORDER BY points DESC, name;")
    assert got.rows[0] == ("James Chepkoech", "84")
    assert got.rows[1:3] == [("Njoroge Kilonzo", "82"), ("Sharon Nduta", "82")], "ties go in alphabetical order"


def test_top_ten(results, target):
    got = same(results, target / "1-top_ten.sql",
               "SELECT name, school, points FROM results ORDER BY points DESC, name LIMIT 10;")
    assert len(got.rows) == 10


def test_next_ten(results, target):
    got = same(results, target / "2-next_ten.sql",
               "SELECT name, points FROM results ORDER BY points DESC, name LIMIT 10 OFFSET 10;")
    assert got.rows[0] == ("Daniel Wanjiru", "74")


def test_counties_once_each(results, target):
    got = same(results, target / "3-counties.sql", "SELECT DISTINCT county FROM results ORDER BY county;")
    assert got.column(0) == ["Kiambu", "Kisumu", "Nairobi", "Nandi", "Uasin Gishu", "Vihiga"]


def test_a_grades(results, target):
    same(results, target / "4-a_grades.sql",
         "SELECT name, grade, points FROM results WHERE grade IN ('A', 'A-') ORDER BY points DESC, name;")


def test_kata_runner_up(results, target):
    got = results.run_file(target / "kata.sql").check()
    assert got.columns == ["second_best"]
    assert got.rows == [("82",)], "two candidates share 82, and 84 is the best, so the runner-up score is 82"


def test_kata_runner_up_with_a_tie_at_the_top(results, target):
    results.run("INSERT INTO results VALUES (26, 'Baraka Ochieng', 'Maseno School', 'Kisumu', 84, 'A');").check()
    got = results.run_file(target / "kata.sql").check()
    assert got.rows == [("82",)], "with two 84s the second-highest *score* is still 82: use DISTINCT"
