-- Extra: Predict the Output. A small company's staff list (made up), with the awkward cases on purpose:
-- a missing salary, a staff member with no department, a department with nobody in it.

CREATE TABLE departments (
    name  VARCHAR(20) PRIMARY KEY,
    floor INT NOT NULL
);

CREATE TABLE staff (
    id     INT PRIMARY KEY,
    name   VARCHAR(30) NOT NULL,
    dept   VARCHAR(20) NULL,
    salary INT NULL,
    FOREIGN KEY (dept) REFERENCES departments (name)
);

INSERT INTO departments VALUES ('Sales', 1), ('Tech', 2), ('Finance', 3), ('Legal', 4);

INSERT INTO staff VALUES
    (1, 'Achieng', 'Sales', 40000),
    (2, 'Baraka', 'Sales', 55000),
    (3, 'Chebet', 'Sales', NULL),
    (4, 'Daudi', 'Tech', 90000),
    (5, 'Esther', 'Tech', 70000),
    (6, 'Faraji', 'Tech', 70000),
    (7, 'Gathoni', 'Finance', 60000),
    (8, 'Hamisi', NULL, 30000),
    (9, 'Imani', 'Finance', NULL);
