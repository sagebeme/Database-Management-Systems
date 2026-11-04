-- Registered patients with no visits. Alphabetical.
-- Columns: name
SELECT p.name
FROM patients AS p
WHERE NOT EXISTS (SELECT 1 FROM visits AS v WHERE v.patient_id = p.id)
ORDER BY p.name;
