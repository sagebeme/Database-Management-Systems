-- Matatu routes out of Nairobi town. The destinations are real; the route numbers, saccos,
-- fares and distances are made up for practice.
--   tools/mysql.sh matatu < phase-1-first-queries/day-004-matatu-stages/setup.sql
DROP TABLE IF EXISTS routes;
CREATE TABLE routes (
    id INT,
    route_no VARCHAR(5),
    destination VARCHAR(40),
    sacco VARCHAR(40),
    fare_kes INT,
    distance_km DECIMAL(4, 1),
    night_fare_kes INT
);
INSERT INTO routes (id, route_no, destination, sacco, fare_kes, distance_km, night_fare_kes) VALUES
    (1, '11', 'Ngong', 'Neema Line', 100, 22.0, 150),
    (2, '14', 'Kitengela', 'Kasi Sacco', 120, 30.5, 200),
    (3, '23', 'Kawangware', 'Umoja Express', 50, 9.0, 80),
    (4, '25', 'Rongai', 'Neema Line', 100, 18.5, NULL),
    (5, '31', 'Thika', 'Mwananchi Shuttle', 150, 44.0, 250),
    (6, '33', 'Embakasi', 'Kasi Sacco', 70, 14.0, 100),
    (7, '40', 'Githurai', 'Umoja Express', 60, 13.5, NULL),
    (8, '42', 'Kikuyu', 'Mwananchi Shuttle', 80, 20.0, 120),
    (9, '45', 'Westlands', 'Umoja Express', 40, 4.5, NULL),
    (10, '48', 'Ruaka', 'Neema Line', 70, 15.0, 100),
    (11, '52', 'Ngong', 'Kasi Sacco', 90, 22.0, NULL),
    (12, '57', 'Kiserian', 'Neema Line', 130, 32.0, 180);
