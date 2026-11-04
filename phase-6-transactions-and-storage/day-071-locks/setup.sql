-- Two SACCO accounts that send each other money all day (invented).
--   tools/mysql.sh locks < phase-6-transactions-and-storage/day-071-locks/setup.sql
DROP TABLE IF EXISTS accounts;
CREATE TABLE accounts (
    phone CHAR(12) PRIMARY KEY,
    balance INT NOT NULL
);
INSERT INTO accounts VALUES ('254711000001', 10000), ('254722000002', 10000);
