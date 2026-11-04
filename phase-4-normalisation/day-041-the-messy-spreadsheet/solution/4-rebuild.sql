-- Join the split tables back into the spreadsheet's shape: student, student_phone, subject, fee, tutor, tutor_room.
-- Ordered by student, then subject.
SELECT s.name AS student, s.phone AS student_phone, sub.name AS subject, sub.fee, t.name AS tutor, t.room AS tutor_room
FROM registrations AS r
JOIN students AS s ON s.name = r.student
JOIN subjects AS sub ON sub.name = r.subject
JOIN tutors AS t ON t.name = sub.tutor
ORDER BY student, subject;
