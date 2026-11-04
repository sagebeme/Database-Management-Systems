"""Day 61: Average Scores."""

import re

import pytest

AVERAGES = "SELECT name, average_score FROM users ORDER BY id;"
# Mutua's first correction, a heavier project, and a stale average to overwrite.
SHAKE_UP = """INSERT INTO projects (name, weight) VALUES ('Indexes', 4);
INSERT INTO corrections VALUES (4, 4, 60), (2, 4, 100), (4, 1, 90);
UPDATE users SET average_score = 99 WHERE name = 'Chebet';"""


@pytest.fixture
def school(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def install(db, folder, name):
    db.run_file(folder / f"{name}.sql").check()
    db.run_file(folder / f"{name}.sql").check()


def body(target, name):
    return (target / f"{name}.sql").read_text().split("this line.")[-1]


def test_average_score(school, target):
    install(school, target, "0-average_score")
    school.run("CALL ComputeAverageScoreForUser(1); CALL ComputeAverageScoreForUser(3);").check()
    school.run("CALL ComputeAverageScoreForUser(4);").check()
    assert school.run(AVERAGES).check().rows == [
        ("Wanjiku", "82.00"), ("Otieno", "0.00"), ("Chebet", "83.33"), ("Mutua", "0.00")], "only the users asked for"
    school.run("INSERT INTO corrections VALUES (1, 1, 100);").check()
    school.run("CALL ComputeAverageScoreForUser(1);").check()
    assert school.run(AVERAGES).check().rows[0] == ("Wanjiku", "86.50")


def test_safe_div(school, target):
    install(school, target, "1-safe_div")
    assert school.run("SELECT SafeDiv(10, 4), SafeDiv(3, 0), SafeDiv(-7, 2), SafeDiv(0, 5);").check().rows == [
        ("2.5", "0", "-3.5", "0")]
    assert school.run("SELECT routine_type, is_deterministic FROM information_schema.routines "
                      "WHERE routine_schema = DATABASE() AND routine_name = 'SafeDiv';").check().rows == [
        ("FUNCTION", "YES")]


def test_weighted_average(school, target):
    install(school, target, "2-weighted_average")
    for user in range(1, 5):
        school.run(f"CALL ComputeAverageWeightedScoreForUser({user});").check()
    assert school.run(AVERAGES).check().rows == [
        ("Wanjiku", "80.33"), ("Otieno", "59.00"), ("Chebet", "83.00"), ("Mutua", "0.00")]


def test_all_users_cursor(school, day, target):
    assert re.search(r"\bCURSOR\s+FOR\b", body(target, "3-all_users_cursor"), re.I), "use a cursor"
    school.load(day / "solution" / "2-weighted_average.sql")
    install(school, target, "3-all_users_cursor")
    school.run("CALL ComputeAverageWeightedScoreForUsers();").check()
    assert school.run(AVERAGES).check().rows == [
        ("Wanjiku", "80.33"), ("Otieno", "59.00"), ("Chebet", "83.00"), ("Mutua", "0.00")]
    school.run(SHAKE_UP).check()
    school.run("CALL ComputeAverageWeightedScoreForUsers();").check()
    assert school.run(AVERAGES).check().rows == [
        ("Wanjiku", "80.33"), ("Otieno", "82.43"), ("Chebet", "83.00"), ("Mutua", "66.00")]


def test_grade(school, target):
    install(school, target, "4-grade")
    assert school.run("SELECT Grade(100), Grade(80), Grade(79.99), Grade(65), Grade(50), Grade(49.5), Grade(40), "
                      "Grade(39.99), Grade(0);").check().rows == [("A", "A", "B", "B", "C", "D", "D", "E", "E")]
    assert school.run("SELECT Grade(score) AS g, COUNT(*) FROM corrections GROUP BY g ORDER BY g;").check().rows == [
        ("A", "4"), ("B", "2"), ("C", "2")]


def test_kata_all_in_one_go(school, day, target):
    text = body(target, "kata")
    assert not re.search(r"\b(CURSOR|LOOP|WHILE|REPEAT|CALL)\b", text, re.I), "one UPDATE, no loop"
    install(school, target, "kata")
    school.run(SHAKE_UP).check()
    school.run("CALL ComputeAllInOneGo();").check()
    yours = school.run(AVERAGES).check().rows
    school.load(day / "solution" / "2-weighted_average.sql")
    school.load(day / "solution" / "3-all_users_cursor.sql")
    school.run("UPDATE users SET average_score = 42;").check()
    school.run("CALL ComputeAverageWeightedScoreForUsers();").check()
    assert yours == school.run(AVERAGES).check().rows
    school.run("DELETE FROM corrections WHERE user_id = 4;").check()
    school.run("CALL ComputeAllInOneGo();").check()
    assert school.run(AVERAGES).check().rows[3] == ("Mutua", "0.00"), "no corrections now: back to 0"
