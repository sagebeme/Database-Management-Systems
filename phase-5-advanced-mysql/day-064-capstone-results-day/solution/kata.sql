-- Most improved: the student (or students, if tied) whose mean rose the most from the Opener to the Midterm:
-- name, form, opener, midterm, gain (all 2 decimal places). Ties by name.
-- Write your statement below this line.
WITH means AS (
    SELECT r.student_id,
           AVG(CASE WHEN e.name = 'Opener' THEN r.score END) AS opener,
           AVG(CASE WHEN e.name = 'Midterm' THEN r.score END) AS midterm
    FROM results AS r
    JOIN exams AS e ON e.id = r.exam_id
    GROUP BY r.student_id
), gains AS (
    SELECT student_id, opener, midterm, midterm - opener AS gain,
           RANK() OVER (ORDER BY midterm - opener DESC) AS r
    FROM means
)
SELECT s.name, s.form, ROUND(g.opener, 2) AS opener, ROUND(g.midterm, 2) AS midterm, ROUND(g.gain, 2) AS gain
FROM gains AS g
JOIN students AS s ON s.id = g.student_id
WHERE g.r = 1
ORDER BY s.name;
