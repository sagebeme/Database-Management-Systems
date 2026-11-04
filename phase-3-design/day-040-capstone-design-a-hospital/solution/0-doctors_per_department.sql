-- Every department and how many doctors it has, zero included. Most first, ties alphabetical.
-- Columns: department, doctors
SELECT d.name AS department, COUNT(doc.id) AS doctors
FROM departments AS d
LEFT JOIN doctors AS doc ON doc.department_id = d.id
GROUP BY d.id, d.name
ORDER BY doctors DESC, department;
