-- A view, need_meet: students whose mean in the latest exam (by sat_on) is below 50, and who have never met
-- their class teacher or last met them more than 30 days before that exam: name, form, mean (2 decimal places).
-- Write your statement below this line.
CREATE OR REPLACE VIEW need_meet AS
SELECT s.name, s.form, ROUND(AVG(r.score), 2) AS mean
FROM students AS s
JOIN results AS r ON r.student_id = s.id
JOIN exams AS e ON e.id = r.exam_id
WHERE e.sat_on = (SELECT MAX(sat_on) FROM exams)
  AND (s.last_meeting IS NULL OR s.last_meeting < e.sat_on - INTERVAL 30 DAY)
GROUP BY s.id, s.name, s.form
HAVING AVG(r.score) < 50;
