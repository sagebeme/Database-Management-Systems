-- A tuition centre's tutor list (invented people). Each row: a tutor, a subject they teach, a language they
-- teach in. Subjects and languages have nothing to do with each other, so every pair has to be listed.
--   tools/mysql.sh tuition < phase-4-normalisation/day-050-fourth-normal-form/setup.sql
DROP TABLE IF EXISTS tutor_subjects, tutor_languages, tutor_offers;
CREATE TABLE tutor_offers (
    tutor VARCHAR(40) NOT NULL,
    subject VARCHAR(40) NOT NULL,
    language VARCHAR(40) NOT NULL,
    PRIMARY KEY (tutor, subject, language)
);
INSERT INTO tutor_offers VALUES
    ('Achieng', 'Maths', 'English'), ('Achieng', 'Maths', 'Kiswahili'), ('Achieng', 'Maths', 'Dholuo'),
    ('Achieng', 'Physics', 'English'), ('Achieng', 'Physics', 'Kiswahili'), ('Achieng', 'Physics', 'Dholuo'),
    ('Baraka', 'Chemistry', 'English'), ('Baraka', 'Chemistry', 'Kiswahili'),
    ('Wanjiru', 'Maths', 'English'), ('Wanjiru', 'Biology', 'English'), ('Wanjiru', 'Chemistry', 'English');
