-- Split enrolments into student_course (student, course) and course_lecturer (course, lecturer) instead.
CREATE TABLE student_course AS SELECT DISTINCT student, course FROM enrolments;
CREATE TABLE course_lecturer AS SELECT DISTINCT course, lecturer FROM enrolments;
