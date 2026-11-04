-- Wanjiru Kamau's visits (look her up by name), oldest first.
-- Columns: visited_at, doctor, department, diagnosis
SELECT v.visited_at, doc.name AS doctor, d.name AS department, v.diagnosis
FROM visits AS v
JOIN patients AS p ON p.id = v.patient_id
JOIN doctors AS doc ON doc.id = v.doctor_id
JOIN departments AS d ON d.id = doc.department_id
WHERE p.name = 'Wanjiru Kamau'
ORDER BY v.visited_at;
