-- Matatu saccos and their routes. The route numbers are real Nairobi ones; the saccos, and every fare, are made up.
--   tools/psql.sh matatu -f phase-7-beyond-mysql/day-079-postgresql-for-mysql-users/setup.sql
DROP TABLE IF EXISTS routes, saccos CASCADE;
CREATE TABLE saccos (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE routes (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    number TEXT NOT NULL UNIQUE,
    destination TEXT NOT NULL,
    sacco_id INT NOT NULL REFERENCES saccos (id),
    fare INT NOT NULL CHECK (fare > 0)
);
INSERT INTO saccos (name) VALUES ('Mwendo Express'), ('Jiji Shuttle'), ('Pwani Ride'), ('Kilele Movers');
INSERT INTO routes (number, destination, sacco_id, fare) VALUES
    ('46', 'Kawangware', 1, 70),
    ('33', 'Embakasi', 1, 80),
    ('19C', 'Komarock', 1, 70),
    ('111', 'Ngong', 2, 100),
    ('105', 'Kikuyu', 2, 100),
    ('125', 'Ongata Rongai', 3, 120),
    ('126', 'Rongai via Lang''ata', 3, 100),
    ('58', 'Buruburu', 4, 60),
    ('237', 'Thika', 4, 150);
