-- Ziwani County's government (an invented county; invented people and salaries in shillings a month), and one
-- kiosk's takings from Day 55.
--   tools/mysql.sh county < phase-5-advanced-mysql/day-056-who-reports-to-whom/setup.sql
DROP TABLE IF EXISTS employees, takings;
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    title VARCHAR(60) NOT NULL,
    department VARCHAR(30) NOT NULL,
    salary INT NOT NULL,
    manager_id INT NULL,
    FOREIGN KEY (manager_id) REFERENCES employees (id)
);
INSERT INTO employees VALUES
    (1, 'Amina Hassan', 'Governor', 'Executive', 450000, NULL),
    (2, 'Peter Kamau', 'CEC Health', 'Health', 300000, 1),
    (3, 'Grace Achieng', 'CEC Roads', 'Roads', 300000, 1),
    (4, 'John Mwangi', 'Chief Officer Health', 'Health', 220000, 2),
    (5, 'Mercy Chebet', 'Director Hospitals', 'Health', 180000, 4),
    (6, 'David Otieno', 'Director Public Health', 'Health', 175000, 4),
    (7, 'Faith Wairimu', 'Medical Superintendent', 'Health', 160000, 5),
    (8, 'Brian Kiprono', 'Clinical Officer', 'Health', 85000, 7),
    (9, 'Lucy Njeri', 'Nurse', 'Health', 70000, 7),
    (10, 'Samuel Mutua', 'Health Inspector', 'Health', 65000, 6),
    (11, 'Hassan Ali', 'Chief Officer Roads', 'Roads', 220000, 3),
    (12, 'Esther Wanjiru', 'Roads Engineer', 'Roads', 140000, 11),
    (13, 'Kevin Omondi', 'Surveyor', 'Roads', 90000, 12),
    (14, 'Janet Akinyi', 'Driver', 'Roads', 45000, 11),
    (15, 'Moses Kiptoo', 'Chief of Staff', 'Executive', 250000, 1);
CREATE TABLE takings (
    day DATE PRIMARY KEY,
    amount INT NOT NULL
);
INSERT INTO takings VALUES
    ('2026-03-02', 4000), ('2026-03-03', 4700), ('2026-03-04', 4400), ('2026-03-05', 8200), ('2026-03-06', 5400),
    ('2026-03-07', 8800), ('2026-03-09', 4000), ('2026-03-10', 8200), ('2026-03-11', 4600), ('2026-03-12', 5400),
    ('2026-03-13', 4000), ('2026-03-14', 5700);
