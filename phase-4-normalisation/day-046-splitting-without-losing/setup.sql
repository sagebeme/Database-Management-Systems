-- Who takes which course, and who teaches it (invented people). Each course has one lecturer.
--   tools/mysql.sh split < phase-4-normalisation/day-046-splitting-without-losing/setup.sql
DROP TABLE IF EXISTS enrolments, student_lecturer, course_lecturer, student_course;
CREATE TABLE enrolments (
    student VARCHAR(20) NOT NULL,
    course VARCHAR(20) NOT NULL,
    lecturer VARCHAR(20) NOT NULL,
    PRIMARY KEY (student, course)
);
INSERT INTO enrolments VALUES
    ('Achieng', 'Databases', 'Dr Otieno'),
    ('Achieng', 'Networks', 'Dr Wanjiku'),
    ('Baraka', 'Databases', 'Dr Otieno'),
    ('Baraka', 'Compilers', 'Dr Otieno'),
    ('Chebet', 'Networks', 'Dr Wanjiku');
