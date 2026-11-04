-- A SACCO's members and loans. Each loan records the loan officer (a database role) who made it. Made up.
--   tools/psql.sh locked -f phase-8-expert/day-094-lock-it-down/setup.sql
DROP TABLE IF EXISTS loans, members;
CREATE TABLE members (
    id INT PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    id_number TEXT NOT NULL
);
CREATE TABLE loans (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    member_id INT NOT NULL REFERENCES members (id),
    amount INT NOT NULL CHECK (amount > 0),
    officer TEXT NOT NULL DEFAULT current_user
);
INSERT INTO members VALUES
    (1, 'Wanjiku Kamau', '254711000001', '23456781'),
    (2, 'Otieno Ochieng', '254722000002', '30987654'),
    (3, 'Chebet Kiprop', '254733000003', '28765432');
INSERT INTO loans (member_id, amount, officer) VALUES
    (1, 50000, 'sacco_teller'),
    (2, 20000, 'sacco_teller2'),
    (3, 75000, 'sacco_teller'),
    (1, 10000, 'sacco_teller2');
