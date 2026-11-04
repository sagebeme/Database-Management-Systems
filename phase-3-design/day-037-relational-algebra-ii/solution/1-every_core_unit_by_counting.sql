-- The same answer by counting: students whose number of core registrations equals the number of core units.
SELECT s.name
FROM students AS s
JOIN registrations AS r ON r.adm_no = s.adm_no
JOIN units AS u ON u.code = r.code AND u.core
GROUP BY s.adm_no, s.name
HAVING COUNT(*) = (SELECT COUNT(*) FROM units WHERE core)
ORDER BY s.name;
