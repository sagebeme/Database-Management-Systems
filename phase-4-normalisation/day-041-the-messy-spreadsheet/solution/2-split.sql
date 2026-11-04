-- Split the spreadsheet so each fact is stored once: create tutors (name PK, room), subjects (name PK, fee, tutor FK),
-- students (name PK, phone UNIQUE) and registrations (student FK, subject FK, both the key), then fill them from registrations_flat.
CREATE TABLE tutors (
    name VARCHAR(40) PRIMARY KEY,
    room CHAR(3) NOT NULL
);
CREATE TABLE subjects (
    name VARCHAR(20) PRIMARY KEY,
    fee INT NOT NULL,
    tutor VARCHAR(40) NOT NULL,
    FOREIGN KEY (tutor) REFERENCES tutors (name)
);
CREATE TABLE students (
    name VARCHAR(40) PRIMARY KEY,
    phone CHAR(12) NOT NULL UNIQUE
);
CREATE TABLE registrations (
    student VARCHAR(40) NOT NULL,
    subject VARCHAR(20) NOT NULL,
    PRIMARY KEY (student, subject),
    FOREIGN KEY (student) REFERENCES students (name),
    FOREIGN KEY (subject) REFERENCES subjects (name)
);
INSERT INTO tutors SELECT DISTINCT tutor, tutor_room FROM registrations_flat;
INSERT INTO subjects SELECT DISTINCT subject, fee, tutor FROM registrations_flat;
INSERT INTO students SELECT DISTINCT student, student_phone FROM registrations_flat;
INSERT INTO registrations SELECT student, subject FROM registrations_flat;
