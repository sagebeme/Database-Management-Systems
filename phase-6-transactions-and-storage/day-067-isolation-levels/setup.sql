-- One account and one trip's bookings. Plain SQL that MySQL and PostgreSQL both accept; the tests load it
-- into each.
--   tools/mysql.sh levels < phase-6-transactions-and-storage/day-067-isolation-levels/setup.sql
--   psql -h 127.0.0.1 -p 5434 -U postgres -d levels -f phase-6-transactions-and-storage/day-067-isolation-levels/setup.sql
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
    phone CHAR(12) PRIMARY KEY,
    balance INT NOT NULL
);
CREATE TABLE bookings (
    id INT PRIMARY KEY,
    trip_id INT NOT NULL,
    passenger VARCHAR(40) NOT NULL
);
INSERT INTO accounts VALUES ('254711000001', 1500);
INSERT INTO bookings VALUES (1, 2, 'Wanjiku'), (2, 2, 'Otieno'), (3, 1, 'Chebet');
CREATE TABLE doctors (
    name VARCHAR(40) PRIMARY KEY,
    on_call BOOLEAN NOT NULL
);
INSERT INTO doctors VALUES ('Dr Achieng', TRUE), ('Dr Barasa', TRUE);
