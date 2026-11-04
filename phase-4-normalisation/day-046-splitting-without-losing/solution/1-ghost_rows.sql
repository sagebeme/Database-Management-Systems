-- Join student_lecturer and course_lecturer back together and list the rows that were never in enrolments:
-- student, course, lecturer, ordered by student then course.
SELECT sl.student, cl.course, sl.lecturer
FROM student_lecturer AS sl
JOIN course_lecturer AS cl ON cl.lecturer = sl.lecturer
WHERE NOT EXISTS (
    SELECT 1 FROM enrolments AS e
    WHERE e.student = sl.student AND e.course = cl.course AND e.lecturer = sl.lecturer
)
ORDER BY sl.student, cl.course;
