-- Rows for the tables you create today. The county codes and town names are real.
-- Run it AFTER 0-counties_table.sql and 1-towns_table.sql:
--   tools/mysql.sh places < phase-2-many-tables/day-017-counties-and-towns/data.sql
INSERT INTO counties (id, code, name) VALUES
    (1, '001', 'Mombasa'),
    (2, '016', 'Machakos'),
    (3, '022', 'Kiambu'),
    (4, '027', 'Uasin Gishu'),
    (5, '032', 'Nakuru'),
    (6, '042', 'Kisumu'),
    (7, '047', 'Nairobi');
INSERT INTO towns (id, county_id, name) VALUES
    (1, 1, 'Mombasa'),
    (2, 2, 'Machakos'),
    (3, 2, 'Athi River'),
    (4, 3, 'Thika'),
    (5, 3, 'Ruiru'),
    (6, 3, 'Kikuyu'),
    (7, 3, 'Limuru'),
    (8, 4, 'Eldoret'),
    (9, 5, 'Nakuru'),
    (10, 5, 'Naivasha'),
    (11, 5, 'Molo'),
    (12, 6, 'Kisumu'),
    (13, 6, 'Maseno');
