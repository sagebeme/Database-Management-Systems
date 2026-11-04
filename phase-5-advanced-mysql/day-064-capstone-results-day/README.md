# Day 64: Capstone: Results Day

## The brief

It's results day at a secondary school, for Form Three (3W and 3E): two exams so far (the Opener and the Midterm), four subjects, eight students. Every year the deputy principal spends a weekend with a spreadsheet: grading every paper by hand, ranking each form, printing report cards, and listing who needs to see their class teacher. Every year there are mistakes.

Your job is to make the **database** do all of it, and keep doing it as marks come in. It's Phase 5 in one go: a function, triggers, constraints and indexes, a procedure, views with window functions, and a CTE for the kata.

## What you'll use

- **Day 61**: functions (`Grade`). **Days 58–59**: triggers that set `NEW` values.
- **Day 53**: unique constraints. **Day 62**: indexes.
- **Day 60**: procedures that return rows. **Day 26**: views. **Day 54**: `RANK()`.
- **Day 57**: date arithmetic. **Day 56**: CTEs.
- **A view with a window function** is fine: `CREATE OR REPLACE VIEW exam_ranking AS SELECT ..., RANK() OVER (...) AS position FROM ... GROUP BY ...;`. The window runs after the grouping, so it can rank by `SUM(r.score)`.
- **"The latest exam"** is the one with the biggest `sat_on`: `(SELECT MAX(sat_on) FROM exams)`. Don't write `exam_id = 2`; a third exam is coming.
- **"More than 30 days before the exam"** is `last_meeting < sat_on - INTERVAL 30 DAY`. A teacher who met a student exactly 30 days before has met them recently enough.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS results;"
tools/mysql.sh results < phase-5-advanced-mysql/day-064-capstone-results-day/setup.sql
```

1. `starter/0-grades.sql`: `Grade(score)`, the triggers `grade_on_insert` and `grade_on_update`, and grades for the results already there. A grade must never disagree with its score, even if someone tries to type one in.
2. `starter/1-one_result_each.sql`: `uq_result` (one result per student, subject and exam) and `idx_results_exam` (exam, then student).
3. `starter/2-report_card.sql`: `ReportCard(student_name, exam_name)`.
4. `starter/3-exam_ranking.sql`: the view `exam_ranking`, with each student's position in their form for each exam.
5. `starter/4-need_meet.sql`: the view `need_meet`.
6. `pytest phase-5-advanced-mysql/day-064-capstone-results-day`

Then try it like the deputy principal would: `CALL ReportCard('Kiprop Bett', 'Midterm');`, `SELECT * FROM exam_ranking WHERE exam = 'Midterm' AND form = '3W' ORDER BY position;`, `SELECT * FROM need_meet;`.

## The kata: Most Improved

In `starter/kata.sql`, find the student whose mean rose the most from the Opener to the Midterm (all of them, if tied): `name`, `form`, `opener`, `midterm`, `gain`. A CTE with one row per student and both means (`AVG(CASE WHEN e.name = 'Opener' THEN r.score END)`) makes the rest easy.

## When you're stuck

- **Old results have no grade**: the triggers only grade new inserts and updates. Grade the existing rows once, with an `UPDATE`.
- **Someone can still set `grade = 'A'` by hand**: the `BEFORE UPDATE` trigger must set `NEW.grade = Grade(NEW.score)` every time, whatever the `UPDATE` said.
- **`ERROR 1062` when creating `uq_result`**: the data already has a duplicate. It shouldn't if you started from a fresh `setup.sql`, so reload it.
- **Positions are 1 to 8 instead of 1 to 4**: `PARTITION BY` the exam *and* the form.
- **`ERROR 1356: View ... references invalid table(s) or column(s)`**: a table or column the view uses was renamed or dropped after you created it. Recreate the view.
- **`need_meet` misses Otieno**: he has never had a meeting, so `last_meeting` is `NULL`, and `NULL < anything` isn't true. Test `IS NULL` too.
- **After the Endterm, `need_meet` still shows Midterm students**: you hard-coded the exam. Use the latest `sat_on`.
- **The kata shows everyone**: rank the gains and keep `RANK() = 1`, or compare with the `MAX` gain.
