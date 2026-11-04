-- A small SACCO: members, their loans and repayments. Made up.
--   tools/psql.sh sacco -f phase-8-expert/day-093-never-lose-data/setup.sql
DROP TABLE IF EXISTS repayments, loans, members;
CREATE TABLE members (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL UNIQUE
);
CREATE TABLE loans (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    member_id INT NOT NULL REFERENCES members (id),
    amount INT NOT NULL CHECK (amount > 0),
    taken_on DATE NOT NULL
);
CREATE TABLE repayments (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    loan_id INT NOT NULL REFERENCES loans (id),
    amount INT NOT NULL CHECK (amount > 0),
    paid_on DATE NOT NULL
);
INSERT INTO members (name, phone)
SELECT 'Member ' || i, '2547' || lpad((i * 7919 % 100000000)::text, 8, '0') FROM generate_series(1, 300) AS i;
INSERT INTO loans (member_id, amount, taken_on)
SELECT 1 + (i * 37) % 300, 5000 + (i * 113) % 95000, DATE '2025-01-01' + (i * 7) % 400 FROM generate_series(1, 500) AS i;
INSERT INTO repayments (loan_id, amount, paid_on)
SELECT 1 + (i * 11) % 500, 500 + (i * 29) % 4500, DATE '2025-02-01' + (i * 3) % 400 FROM generate_series(1, 2000) AS i;
