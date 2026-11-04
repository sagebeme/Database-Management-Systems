-- Join student_course and course_lecturer back: student, course, lecturer, ordered by student then course.
SELECT sc.student, sc.course, cl.lecturer
FROM student_course AS sc
JOIN course_lecturer AS cl ON cl.course = sc.course
ORDER BY sc.student, sc.course;
