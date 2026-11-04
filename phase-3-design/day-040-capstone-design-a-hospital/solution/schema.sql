-- The hospital's tables. The README lists the tables and columns the app expects; the keys,
-- types and constraints are yours to choose. Make the rules in the brief impossible to break.
CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(40) NOT NULL UNIQUE
);

CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    licence_no VARCHAR(10) NOT NULL UNIQUE,
    department_id INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments (id)
);

CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    national_id VARCHAR(10) NULL UNIQUE,
    born_on DATE NOT NULL,
    phone CHAR(12) NULL CHECK (phone REGEXP '^254[17][0-9]{8}$')
);

CREATE TABLE next_of_kin (
    patient_id INT NOT NULL,
    name VARCHAR(60) NOT NULL,
    relationship VARCHAR(20) NOT NULL,
    phone CHAR(12) NOT NULL,
    PRIMARY KEY (patient_id, name),
    FOREIGN KEY (patient_id) REFERENCES patients (id) ON DELETE CASCADE
);

CREATE TABLE visits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    visited_at DATETIME NOT NULL,
    diagnosis VARCHAR(100) NULL,
    FOREIGN KEY (patient_id) REFERENCES patients (id),
    FOREIGN KEY (doctor_id) REFERENCES doctors (id)
);

CREATE TABLE drugs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(60) NOT NULL UNIQUE,
    unit_price DECIMAL(8, 2) NOT NULL CHECK (unit_price >= 0)
);

CREATE TABLE prescriptions (
    visit_id INT NOT NULL,
    drug_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (visit_id, drug_id),
    FOREIGN KEY (visit_id) REFERENCES visits (id),
    FOREIGN KEY (drug_id) REFERENCES drugs (id)
);
