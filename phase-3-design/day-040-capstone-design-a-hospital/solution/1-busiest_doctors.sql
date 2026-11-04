-- Every doctor and how many visits they've seen, zero included. Most first, ties alphabetical.
-- Columns: doctor, visits
SELECT doc.name AS doctor, COUNT(v.id) AS visits
FROM doctors AS doc
LEFT JOIN visits AS v ON v.doctor_id = doc.id
GROUP BY doc.id, doc.name
ORDER BY visits DESC, doctor;
