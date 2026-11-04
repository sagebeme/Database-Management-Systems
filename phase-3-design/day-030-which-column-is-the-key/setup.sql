-- Matatu saccos (invented names) for Day 30.
--   tools/mysql.sh fleet < phase-3-design/day-030-which-column-is-the-key/setup.sql
DROP TABLE IF EXISTS vehicles, saccos;
CREATE TABLE saccos (
    id INT PRIMARY KEY,
    name VARCHAR(60) NOT NULL UNIQUE
);
INSERT INTO saccos VALUES (1, 'Mwangaza Shuttle'), (2, 'Pwani Express'), (3, 'Rift Riders');
