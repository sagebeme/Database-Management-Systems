-- Form Three's results at an invented secondary school: two exams, four subjects, eight students.
-- last_meeting is the last time a student met their class teacher about their marks.
--   tools/mysql.sh results < phase-5-advanced-mysql/day-064-capstone-results-day/setup.sql
DROP VIEW IF EXISTS need_meet, exam_ranking;
DROP TABLE IF EXISTS results, exams, subjects, students;
CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    form CHAR(2) NOT NULL,
    last_meeting DATE NULL
);
CREATE TABLE subjects (
    id INT PRIMARY KEY,
    name VARCHAR(30) NOT NULL UNIQUE
);
CREATE TABLE exams (
    id INT PRIMARY KEY,
    name VARCHAR(30) NOT NULL UNIQUE,
    sat_on DATE NOT NULL
);
CREATE TABLE results (
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    exam_id INT NOT NULL,
    score INT NOT NULL CHECK (score BETWEEN 0 AND 100),
    grade CHAR(1) NULL,
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (subject_id) REFERENCES subjects (id),
    FOREIGN KEY (exam_id) REFERENCES exams (id)
);
INSERT INTO students VALUES
    (1, 'Wanjiku Kamau', '3W', '2026-01-12'),
    (2, 'Otieno Ouma', '3W', NULL),
    (3, 'Chebet Rono', '3W', NULL),
    (4, 'Mutua Musyoka', '3W', '2026-02-20'),
    (5, 'Akinyi Atieno', '3E', NULL),
    (6, 'Hassan Ali', '3E', '2025-11-03'),
    (7, 'Njeri Wambui', '3E', NULL),
    (8, 'Kiprop Bett', '3E', '2026-02-27');
INSERT INTO subjects VALUES (1, 'Maths'), (2, 'English'), (3, 'Kiswahili'), (4, 'Biology');
INSERT INTO exams VALUES (1, 'Opener', '2026-01-20'), (2, 'Midterm', '2026-03-02');
INSERT INTO results (student_id, subject_id, exam_id, score) VALUES
    (1, 1, 1, 81),
    (1, 2, 1, 69),
    (1, 3, 1, 86),
    (1, 4, 1, 85),
    (2, 1, 1, 45),
    (2, 2, 1, 50),
    (2, 3, 1, 54),
    (2, 4, 1, 33),
    (3, 1, 1, 60),
    (3, 2, 1, 62),
    (3, 3, 1, 76),
    (3, 4, 1, 74),
    (4, 1, 1, 52),
    (4, 2, 1, 34),
    (4, 3, 1, 50),
    (4, 4, 1, 52),
    (5, 1, 1, 66),
    (5, 2, 1, 50),
    (5, 3, 1, 48),
    (5, 4, 1, 59),
    (6, 1, 1, 44),
    (6, 2, 1, 36),
    (6, 3, 1, 53),
    (6, 4, 1, 30),
    (7, 1, 1, 75),
    (7, 2, 1, 85),
    (7, 3, 1, 94),
    (7, 4, 1, 73),
    (8, 1, 1, 37),
    (8, 2, 1, 40),
    (8, 3, 1, 38),
    (8, 4, 1, 53),
    (1, 1, 2, 67),
    (1, 2, 2, 84),
    (1, 3, 2, 74),
    (1, 4, 2, 73),
    (2, 1, 2, 59),
    (2, 2, 2, 48),
    (2, 3, 2, 44),
    (2, 4, 2, 42),
    (3, 1, 2, 76),
    (3, 2, 2, 66),
    (3, 3, 2, 64),
    (3, 4, 2, 58),
    (4, 1, 2, 40),
    (4, 2, 2, 54),
    (4, 3, 2, 35),
    (4, 4, 2, 48),
    (5, 1, 2, 63),
    (5, 2, 2, 61),
    (5, 3, 2, 66),
    (5, 4, 2, 59),
    (6, 1, 2, 47),
    (6, 2, 2, 35),
    (6, 3, 2, 46),
    (6, 4, 2, 39),
    (7, 1, 2, 90),
    (7, 2, 2, 79),
    (7, 3, 2, 75),
    (7, 4, 2, 74),
    (8, 1, 2, 54),
    (8, 2, 2, 61),
    (8, 3, 2, 52),
    (8, 4, 2, 53);
