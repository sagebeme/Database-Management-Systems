-- Rebuild the old table from the two new ones: tutor, subject, language, ordered by all three.
-- Write your statement below this line.
SELECT s.tutor, s.subject, l.language
FROM tutor_subjects AS s
JOIN tutor_languages AS l ON l.tutor = s.tutor
ORDER BY s.tutor, s.subject, l.language;
