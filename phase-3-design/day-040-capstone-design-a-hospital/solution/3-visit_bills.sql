-- Every visit's drug bill (quantity times unit price, added up; 0.00 when nothing was prescribed). In visit order.
-- Columns: visit_id, patient, total
SELECT v.id AS visit_id, p.name AS patient, COALESCE(SUM(pr.quantity * dr.unit_price), 0.00) AS total
FROM visits AS v
JOIN patients AS p ON p.id = v.patient_id
LEFT JOIN prescriptions AS pr ON pr.visit_id = v.id
LEFT JOIN drugs AS dr ON dr.id = pr.drug_id
GROUP BY v.id, p.name
ORDER BY v.id;
