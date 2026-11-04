-- Create students (adm_no INT, name VARCHAR(100)) where a student can't be saved without a name.
CREATE TABLE IF NOT EXISTS students (
    adm_no INT,
    name VARCHAR(100) NOT NULL
);
