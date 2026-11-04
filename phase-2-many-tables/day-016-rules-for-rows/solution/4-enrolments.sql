-- Create enrolments (student_id INT, unit_code CHAR(7), enrolled_on DATE) where a student can enrol in a unit only once.
CREATE TABLE IF NOT EXISTS enrolments (
    student_id INT,
    unit_code CHAR(7),
    enrolled_on DATE,
    PRIMARY KEY (student_id, unit_code)
);
