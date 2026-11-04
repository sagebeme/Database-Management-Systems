-- A week of matatu trips logged by a stage clerk (invented vehicles and people), with one typo.
--   tools/mysql.sh stage < phase-4-normalisation/day-042-does-it-depend/setup.sql
DROP TABLE IF EXISTS trips;
CREATE TABLE trips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plate VARCHAR(10) NOT NULL,
    sacco VARCHAR(30) NOT NULL,
    route VARCHAR(5) NOT NULL,
    driver VARCHAR(30) NOT NULL,
    fare INT NOT NULL,
    trip_date DATE NOT NULL
);
INSERT INTO trips (plate, sacco, route, driver, fare, trip_date) VALUES
    ('KDA 101A', 'Mwangaza Shuttle', '46', 'Otieno', 100, '2026-10-05'),
    ('KDA 101A', 'Mwangaza Shuttle', '46', 'Kamau', 100, '2026-10-06'),
    ('KDB 202B', 'Pwani Express', '111', 'Wanjala', 150, '2026-10-05'),
    ('KDB 202B', 'Pwani Expres', '111', 'Wanjala', 150, '2026-10-07'),
    ('KDC 303C', 'Mwangaza Shuttle', '46', 'Otieno', 100, '2026-10-07'),
    ('KDD 404D', 'Rift Riders', '33', 'Chebet', 80, '2026-10-05'),
    ('KDD 404D', 'Rift Riders', '33', 'Chebet', 80, '2026-10-06'),
    ('KDE 505E', 'Pwani Express', '111', 'Mutua', 150, '2026-10-06');
