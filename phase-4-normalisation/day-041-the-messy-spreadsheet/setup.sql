-- A tuition centre's registrations, kept as one big spreadsheet (invented people).
--   tools/mysql.sh tuition < phase-4-normalisation/day-041-the-messy-spreadsheet/setup.sql
DROP TABLE IF EXISTS registrations, subjects, tutors, students, registrations_flat;
CREATE TABLE registrations_flat (
    student VARCHAR(40) NOT NULL,
    student_phone CHAR(12) NOT NULL,
    subject VARCHAR(20) NOT NULL,
    fee INT NOT NULL,
    tutor VARCHAR(40) NOT NULL,
    tutor_room CHAR(3) NOT NULL,
    PRIMARY KEY (student, subject)
);
INSERT INTO registrations_flat VALUES
    ('Amani Kiptoo', '254711000001', 'Maths', 3000, 'Mr Omondi', 'R1'),
    ('Amani Kiptoo', '254711000001', 'Physics', 3500, 'Ms Wairimu', 'R2'),
    ('Baraka Said', '254722000002', 'Maths', 3000, 'Mr Omondi', 'R1'),
    ('Baraka Said', '254722000002', 'Chemistry', 3500, 'Mr Kibet', 'R3'),
    ('Cynthia Njoki', '254733000003', 'Maths', 3000, 'Mr Omondi', 'R1'),
    ('Cynthia Njoki', '254733000003', 'Biology', 3200, 'Mrs Achieng', 'R4'),
    ('Daudi Mwita', '254744000004', 'Physics', 3500, 'Ms Wairimu', 'R2');
