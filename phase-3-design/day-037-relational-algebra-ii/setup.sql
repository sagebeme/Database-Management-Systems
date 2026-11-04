-- First-year registrations at a made-up college, for Day 37.
--   tools/mysql.sh college < phase-3-design/day-037-relational-algebra-ii/setup.sql
DROP TABLE IF EXISTS registrations, units, students;
CREATE TABLE students (adm_no CHAR(5) PRIMARY KEY, name VARCHAR(40) NOT NULL);
CREATE TABLE units (code CHAR(6) PRIMARY KEY, title VARCHAR(60) NOT NULL, core BOOLEAN NOT NULL);
CREATE TABLE registrations (
    adm_no CHAR(5) NOT NULL,
    code CHAR(6) NOT NULL,
    PRIMARY KEY (adm_no, code),
    FOREIGN KEY (adm_no) REFERENCES students (adm_no),
    FOREIGN KEY (code) REFERENCES units (code)
);
INSERT INTO students VALUES ('S0001', 'Achieng'), ('S0002', 'Baraka'), ('S0003', 'Chebet'),
                            ('S0004', 'Duncan'), ('S0005', 'Esther');
INSERT INTO units VALUES ('COM101', 'Programming I', TRUE), ('COM102', 'Databases I', TRUE),
                         ('MAT101', 'Discrete Maths', TRUE), ('ENG110', 'Communication Skills', FALSE);
INSERT INTO registrations VALUES
    ('S0001', 'COM101'), ('S0001', 'COM102'), ('S0001', 'MAT101'), ('S0001', 'ENG110'),
    ('S0002', 'COM101'), ('S0002', 'MAT101'),
    ('S0003', 'COM101'), ('S0003', 'COM102'), ('S0003', 'MAT101'),
    ('S0004', 'ENG110');
