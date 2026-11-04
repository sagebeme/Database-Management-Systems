-- A tiny mobile wallet (invented people). A balance can never go below zero.
--   tools/mysql.sh wallet < phase-6-transactions-and-storage/day-065-send-money/setup.sql
DROP TABLE IF EXISTS transfers, accounts;
CREATE TABLE accounts (
    phone CHAR(12) PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    balance INT NOT NULL CHECK (balance >= 0)
);
CREATE TABLE transfers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    from_phone CHAR(12) NOT NULL,
    to_phone CHAR(12) NOT NULL,
    amount INT NOT NULL,
    reversed BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (from_phone) REFERENCES accounts (phone),
    FOREIGN KEY (to_phone) REFERENCES accounts (phone)
);
INSERT INTO accounts VALUES
    ('254711000001', 'Wanjiku', 5000), ('254722000002', 'Otieno', 1200), ('254733000003', 'Chebet', 0),
    ('254744000004', 'Mutua', 30000), ('254755000005', 'Akinyi', 750);
