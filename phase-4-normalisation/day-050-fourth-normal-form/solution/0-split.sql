-- Replace tutor_offers with two tables, filled from it:
--   tutor_subjects (tutor, subject), primary key both columns
--   tutor_languages (tutor, language), primary key both columns
-- Keep tutor_offers for now (step 1 compares against it).
-- Write your statement below this line.
DROP TABLE IF EXISTS tutor_subjects, tutor_languages;
CREATE TABLE tutor_subjects (
    tutor VARCHAR(40) NOT NULL,
    subject VARCHAR(40) NOT NULL,
    PRIMARY KEY (tutor, subject)
);
CREATE TABLE tutor_languages (
    tutor VARCHAR(40) NOT NULL,
    language VARCHAR(40) NOT NULL,
    PRIMARY KEY (tutor, language)
);
INSERT INTO tutor_subjects SELECT DISTINCT tutor, subject FROM tutor_offers;
INSERT INTO tutor_languages SELECT DISTINCT tutor, language FROM tutor_offers;
