-- People and counties for Day 33 (the people are invented; the county codes are real).
--   tools/mysql.sh design < phase-3-design/day-033-one-many-many-to-many/setup.sql
DROP TABLE IF EXISTS national_ids, constituencies, persons, counties;
CREATE TABLE persons (
    id INT PRIMARY KEY,
    name VARCHAR(60) NOT NULL
);
INSERT INTO persons VALUES (1, 'Akinyi Odhiambo'), (2, 'Brian Kiptoo'), (3, 'Zawadi Mwende');
CREATE TABLE counties (
    code CHAR(3) PRIMARY KEY,
    name VARCHAR(40) NOT NULL UNIQUE
);
INSERT INTO counties VALUES ('042', 'Kisumu'), ('047', 'Nairobi');
