-- A view, exam_ranking: for every exam and student: exam, form, name, total, mean (2 decimal places) and
-- position in their form for that exam (by total; equal totals share a position, and the next is skipped).
-- Write your statement below this line.
CREATE OR REPLACE VIEW exam_ranking AS
SELECT e.name AS exam, s.form, s.name, SUM(r.score) AS total, ROUND(AVG(r.score), 2) AS mean,
       RANK() OVER (PARTITION BY e.id, s.form ORDER BY SUM(r.score) DESC) AS position
FROM results AS r
JOIN students AS s ON s.id = r.student_id
JOIN exams AS e ON e.id = r.exam_id
GROUP BY e.id, e.name, s.id, s.form, s.name;
