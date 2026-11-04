-- Staff of a small medical insurer (invented people) for Day 34.
--   tools/mysql.sh cover < phase-3-design/day-034-dependants-and-managers/setup.sql
DROP TABLE IF EXISTS dependants, employees;
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    title VARCHAR(40) NOT NULL,
    manager_id INT NULL,
    FOREIGN KEY (manager_id) REFERENCES employees (id)
);
INSERT INTO employees VALUES
    (1, 'Grace Wambui', 'Chief Executive', NULL),
    (2, 'Peter Kamau', 'Head of Claims', 1),
    (3, 'Halima Abdi', 'Head of Finance', 1),
    (4, 'Joseph Otieno', 'Senior Claims Officer', 2),
    (5, 'Mercy Chebet', 'Claims Officer', 2),
    (6, 'Daniel Mutua', 'Claims Officer', 2),
    (7, 'Fatuma Hassan', 'Accountant', 3),
    (8, 'Kevin Njoroge', 'Accountant', 3),
    (9, 'Lilian Achieng', 'Claims Clerk', 4),
    (10, 'Samuel Kiprop', 'Driver', 1);
