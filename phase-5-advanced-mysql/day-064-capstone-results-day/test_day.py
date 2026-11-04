"""Day 64: Capstone, Results Day.

Each part is tested on top of the reference versions of the parts before it, so one mistake doesn't sink the rest.
"""

import pytest

RANKING = "SELECT exam, form, name, total, mean, position FROM exam_ranking ORDER BY exam, form, position, name;"
NEED_MEET = "SELECT name, form, mean FROM need_meet ORDER BY name;"
# Hassan catches up with Akinyi in the Midterm (a tie), Chebet drops, and a third exam becomes the latest.
SHAKE_UP = """UPDATE results SET score = score + 41 WHERE student_id = 6 AND exam_id = 2 AND subject_id = 1;
UPDATE results SET score = score + 41 WHERE student_id = 6 AND exam_id = 2 AND subject_id = 2;
UPDATE results SET score = 30 WHERE student_id = 3 AND exam_id = 2;"""
THIRD_EXAM = """INSERT INTO exams VALUES (3, 'Endterm', '2026-04-08');
INSERT INTO results (student_id, subject_id, exam_id, score)
SELECT id, 1, 3, CASE WHEN id IN (4, 8) THEN 35 ELSE 70 END FROM students;"""


@pytest.fixture
def results(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def reference(db, day, *names):
    for name in names:
        db.load(day / "solution" / f"{name}.sql")


def test_grades(results, target):
    results.run_file(target / "0-grades.sql").check()
    results.run_file(target / "0-grades.sql").check()
    assert results.run("SELECT COUNT(*) FROM results WHERE grade IS NULL OR grade <> Grade(score);").check().rows == [
        ("0",)], "every existing result graded"
    assert results.run("SELECT Grade(80), Grade(79), Grade(65), Grade(64), Grade(50), Grade(40), Grade(39);"
                       ).check().rows == [("A", "B", "B", "C", "C", "D", "E")]
    results.run("INSERT INTO exams VALUES (3, 'Mock', '2026-05-01');").check()
    results.run("INSERT INTO results (student_id, subject_id, exam_id, score) VALUES (1, 1, 3, 81), (2, 1, 3, 12);").check()
    results.run("UPDATE results SET score = 66 WHERE exam_id = 3 AND student_id = 2;").check()
    assert results.run("SELECT student_id, grade FROM results WHERE exam_id = 3 ORDER BY 1;").check().rows == [
        ("1", "A"), ("2", "B")]
    results.run("UPDATE results SET grade = 'A' WHERE exam_id = 3 AND student_id = 2;").check()
    assert results.run("SELECT grade FROM results WHERE exam_id = 3 AND student_id = 2;").check().rows == [("B",)], \
        "the grade can't be typed over"


def test_one_result_each(results, target):
    results.run_file(target / "1-one_result_each.sql").check()
    assert not results.run("INSERT INTO results (student_id, subject_id, exam_id, score) VALUES (1, 1, 1, 50);").ok
    columns = results.run("SELECT index_name, column_name FROM information_schema.statistics "
                          "WHERE table_schema = DATABASE() AND index_name IN ('uq_result', 'idx_results_exam') "
                          "ORDER BY index_name, seq_in_index;").check().rows
    assert columns == [("idx_results_exam", "exam_id"), ("idx_results_exam", "student_id"),
                       ("uq_result", "student_id"), ("uq_result", "subject_id"), ("uq_result", "exam_id")]


def test_report_card(results, day, target):
    reference(results, day, "0-grades")
    results.run_file(target / "2-report_card.sql").check()
    results.run_file(target / "2-report_card.sql").check()
    assert results.run("CALL ReportCard('Otieno Ouma', 'Midterm');").check().rows == [
        ("Biology", "42", "D"), ("English", "48", "D"), ("Kiswahili", "44", "D"), ("Maths", "59", "C")]
    assert results.run("CALL ReportCard('Nobody', 'Midterm');").check().rows == []


def test_exam_ranking(results, target):
    results.run_file(target / "3-exam_ranking.sql").check()
    rows = results.run(RANKING).check().rows
    assert len(rows) == 16
    assert rows[:4] == [("Midterm", "3E", "Njeri Wambui", "318", "79.50", "1"),
                        ("Midterm", "3E", "Akinyi Atieno", "249", "62.25", "2"),
                        ("Midterm", "3E", "Kiprop Bett", "220", "55.00", "3"),
                        ("Midterm", "3E", "Hassan Ali", "167", "41.75", "4")]


def test_exam_ranking_ties(results, day, target):
    results.run(SHAKE_UP).check()
    results.run_file(target / "3-exam_ranking.sql").check()
    yours = results.run(RANKING).check().rows
    assert [r for r in yours if r[0] == "Midterm" and r[1] == "3E"][1:4] == [
        ("Midterm", "3E", "Akinyi Atieno", "249", "62.25", "2"), ("Midterm", "3E", "Hassan Ali", "249", "62.25", "2"),
        ("Midterm", "3E", "Kiprop Bett", "220", "55.00", "4")]
    reference(results, day, "3-exam_ranking")
    assert yours == results.run(RANKING).check().rows


def test_need_meet(results, target):
    results.run_file(target / "4-need_meet.sql").check()
    assert results.run(NEED_MEET).check().rows == [("Hassan Ali", "3E", "41.75"), ("Otieno Ouma", "3W", "48.25")]
    results.run("UPDATE students SET last_meeting = '2026-01-31' WHERE name = 'Hassan Ali';").check()
    assert results.run(NEED_MEET).check().rows == [("Otieno Ouma", "3W", "48.25")], "exactly 30 days is recent enough"
    results.run("UPDATE students SET last_meeting = '2026-01-30' WHERE name = 'Hassan Ali';").check()
    assert len(results.run(NEED_MEET).check().rows) == 2, "31 days isn't"


def test_need_meet_follows_the_latest_exam(results, target):
    results.run_file(target / "4-need_meet.sql").check()
    results.run(THIRD_EXAM).check()
    assert results.run(NEED_MEET).check().rows == [("Kiprop Bett", "3E", "35.00"), ("Mutua Musyoka", "3W", "35.00")], \
        "the Endterm is the latest now, and Mutua's February meeting is too long before it"


def test_kata_most_improved(results, target):
    assert results.run_file(target / "kata.sql").check().rows == [("Kiprop Bett", "3E", "42.00", "55.00", "13.00")]
    results.run("UPDATE results SET score = score + 15 WHERE student_id = 2 AND exam_id = 2 AND subject_id = 1;").check()
    assert results.run_file(target / "kata.sql").check().rows == [("Kiprop Bett", "3E", "42.00", "55.00", "13.00")], \
        "Otieno gains 6.50 now: still second"
    results.run("UPDATE results SET score = score + 26 WHERE student_id = 2 AND exam_id = 2 AND subject_id = 2;").check()
    assert results.run_file(target / "kata.sql").check().rows == [
        ("Kiprop Bett", "3E", "42.00", "55.00", "13.00"), ("Otieno Ouma", "3W", "45.50", "58.50", "13.00")], \
        "a tie: both, by name"
