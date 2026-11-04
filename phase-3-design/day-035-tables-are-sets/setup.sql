-- Towns and their counties (real places) for Day 35.
--   tools/mysql.sh sets < phase-3-design/day-035-tables-are-sets/setup.sql
DROP TABLE IF EXISTS towns;
CREATE TABLE towns (
    name VARCHAR(40) NOT NULL,
    county VARCHAR(40) NOT NULL
);
INSERT INTO towns VALUES
    ('Naivasha', 'Nakuru'), ('Gilgil', 'Nakuru'), ('Molo', 'Nakuru'),
    ('Thika', 'Kiambu'), ('Ruiru', 'Kiambu'),
    ('Eldoret', 'Uasin Gishu'), ('Kisumu', 'Kisumu'), ('Maseno', 'Kisumu');
