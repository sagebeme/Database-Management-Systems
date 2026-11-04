-- Split enrolments into student_lecturer (student, lecturer) and course_lecturer (course, lecturer), each fact once.
CREATE TABLE student_lecturer AS SELECT DISTINCT student, lecturer FROM enrolments;
CREATE TABLE course_lecturer AS SELECT DISTINCT course, lecturer FROM enrolments;
