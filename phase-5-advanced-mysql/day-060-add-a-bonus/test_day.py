"""Day 60: Add a Bonus."""

import pytest


@pytest.fixture
def school(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def install(db, target, name):
    db.run_file(target / f"{name}.sql").check()
    db.run_file(target / f"{name}.sql").check()


def scores(db, project):
    return db.run("SELECT u.name, c.score FROM corrections c JOIN users u ON u.id = c.user_id "
                  f"JOIN projects p ON p.id = c.project_id WHERE p.name = '{project}' ORDER BY u.name;").check().rows


def test_add_bonus(school, target):
    install(school, target, "0-add_bonus")
    school.run("CALL AddBonus(1, 'Joins', 5);").check()
    school.run("CALL AddBonus(4, 'Indexes', 77);").check()
    school.run("CALL AddBonus(2, 'Indexes', 64);").check()
    assert school.run("SELECT id, name FROM projects ORDER BY id;").check().rows == [
        ("1", "SQL basics"), ("2", "Joins"), ("3", "Normalisation"), ("4", "Indexes")], "Indexes made once"
    assert scores(school, "Indexes") == [("Mutua", "77"), ("Otieno", "64")]
    assert scores(school, "Joins") == [("Chebet", "72"), ("Otieno", "61"), ("Wanjiku", "96"), ("Wanjiku", "5")]


def test_count_corrections(school, target):
    install(school, target, "1-count_corrections")
    assert school.run("CALL CountCorrections(1, @n); SELECT @n;").check().rows == [("3",)]
    assert school.run("CALL CountCorrections(2, @n); SELECT @n;").check().rows == [("2",)]
    assert school.run("CALL CountCorrections(4, @n); SELECT @n;").check().rows == [("0",)]


def test_top_scorers(school, target):
    install(school, target, "2-top_scorers")
    result = school.run("CALL TopScorers(3);").check()
    assert result.columns == ["name", "project", "score"]
    assert result.rows == [("Wanjiku", "Joins", "96"), ("Chebet", "SQL basics", "90"), ("Chebet", "Normalisation", "88")]
    school.run("INSERT INTO corrections VALUES (4, 1, 90);").check()
    assert school.run("CALL TopScorers(3);").check().rows[1:] == [
        ("Chebet", "SQL basics", "90"), ("Mutua", "SQL basics", "90")], "ties by name"
    assert len(school.run("CALL TopScorers(20);").check().rows) == 9


def test_rename_project(school, target):
    install(school, target, "3-rename_project")
    school.run("CALL RenameProject('Joins', 'Joins and subqueries');").check()
    school.run("CALL RenameProject('SQL basics', 'SQL basics');").check()
    taken = school.run("CALL RenameProject('Normalisation', 'SQL basics');")
    assert not taken.ok and "Name already taken" in taken.stderr and "45000" in taken.stderr
    missing = school.run("CALL RenameProject('Joins', 'Anything');")
    assert not missing.ok and "No such project" in missing.stderr
    assert school.run("SELECT name FROM projects ORDER BY id;").check().rows == [
        ("SQL basics",), ("Joins and subqueries",), ("Normalisation",)]


def test_kata_curve_project(school, target):
    install(school, target, "kata")
    school.run("CALL CurveProject('SQL basics', 80);").check()
    assert scores(school, "SQL basics") == [("Chebet", "95"), ("Otieno", "60"), ("Wanjiku", "85")], "75 -> 80: +5 each"
    school.run("CALL CurveProject('Joins', 90);").check()
    assert scores(school, "Joins") == [("Chebet", "86"), ("Otieno", "75"), ("Wanjiku", "100")], \
        "average 76.33, so +14 (rounded), and 96 stops at 100"
    school.run("CALL CurveProject('Normalisation', 60);").check()
    assert scores(school, "Normalisation") == [("Chebet", "88"), ("Wanjiku", "70")], "already above: no change"
