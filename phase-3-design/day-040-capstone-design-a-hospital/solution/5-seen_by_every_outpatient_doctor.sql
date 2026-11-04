-- Patients seen by every doctor in the Outpatient department. Alphabetical.
-- Columns: name
SELECT p.name
FROM patients AS p
WHERE NOT EXISTS (
    SELECT 1
    FROM doctors AS doc
    JOIN departments AS d ON d.id = doc.department_id
    WHERE d.name = 'Outpatient'
      AND NOT EXISTS (SELECT 1 FROM visits AS v WHERE v.patient_id = p.id AND v.doctor_id = doc.id)
)
ORDER BY p.name;
