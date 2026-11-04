-- Names of students registered for every core unit, alphabetical. (Division, with NOT EXISTS twice.)
SELECT s.name
FROM students AS s
WHERE NOT EXISTS (
    SELECT 1 FROM units AS u
    WHERE u.core
      AND NOT EXISTS (
          SELECT 1 FROM registrations AS r
          WHERE r.adm_no = s.adm_no AND r.code = u.code
      )
)
ORDER BY s.name;
