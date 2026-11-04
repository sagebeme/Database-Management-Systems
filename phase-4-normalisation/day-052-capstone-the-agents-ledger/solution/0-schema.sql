-- The 3NF design, with every rule the business has (see the README's table contract):
--   agents (till, name, location)
--   customers (phone, name)                       phone as 2547XXXXXXXX or 2541XXXXXXXX
--   transactions (code, done_at, till, phone, type, amount, commission)
-- Write your statement below this line.
DROP TABLE IF EXISTS transactions, customers, agents;
CREATE TABLE agents (
    till VARCHAR(10) PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    location VARCHAR(60) NOT NULL
);
CREATE TABLE customers (
    phone CHAR(12) PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    CHECK (phone REGEXP '^254[17][0-9]{8}$')
);
CREATE TABLE transactions (
    code CHAR(10) PRIMARY KEY,
    done_at DATETIME NOT NULL,
    till VARCHAR(10) NOT NULL,
    phone CHAR(12) NOT NULL,
    type ENUM('Deposit', 'Withdrawal') NOT NULL,
    amount INT NOT NULL CHECK (amount > 0),
    commission INT NOT NULL CHECK (commission >= 0),
    FOREIGN KEY (till) REFERENCES agents (till),
    FOREIGN KEY (phone) REFERENCES customers (phone)
);
