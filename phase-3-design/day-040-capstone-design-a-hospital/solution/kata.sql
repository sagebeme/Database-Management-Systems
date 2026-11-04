-- Kata: The Pharmacy Board. Create the view drug_usage: every drug, how many prescriptions name it and how many units in all (0 if none).
-- Columns: drug, prescriptions, units
CREATE VIEW drug_usage AS
SELECT dr.name AS drug, COUNT(pr.visit_id) AS prescriptions, COALESCE(SUM(pr.quantity), 0) AS units
FROM drugs AS dr
LEFT JOIN prescriptions AS pr ON pr.drug_id = dr.id
GROUP BY dr.id, dr.name;
