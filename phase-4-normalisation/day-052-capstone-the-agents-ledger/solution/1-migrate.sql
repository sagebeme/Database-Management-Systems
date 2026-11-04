-- Move everything from ledger_raw into the new tables, cleaned: no stray spaces, phones as 254..., dates as
-- DATETIME, types as 'Deposit' or 'Withdrawal', amounts and commissions as numbers. ledger_raw stays as it is.
-- Write your statement below this line.
INSERT INTO agents (till, name, location)
SELECT DISTINCT TRIM(till), TRIM(agent_name), TRIM(location) FROM ledger_raw;

INSERT INTO customers (phone, name)
SELECT DISTINCT CASE
               WHEN p LIKE '+254%' THEN SUBSTRING(p, 2)
               WHEN p LIKE '0%' THEN CONCAT('254', SUBSTRING(p, 2))
               ELSE p
           END,
       TRIM(customer_name)
FROM (SELECT REPLACE(TRIM(phone), ' ', '') AS p, customer_name FROM ledger_raw) AS r;

INSERT INTO transactions (code, done_at, till, phone, type, amount, commission)
SELECT TRIM(code),
       STR_TO_DATE(TRIM(date_time), '%d/%m/%Y %H:%i'),
       TRIM(till),
       CASE
               WHEN p LIKE '+254%' THEN SUBSTRING(p, 2)
               WHEN p LIKE '0%' THEN CONCAT('254', SUBSTRING(p, 2))
               ELSE p
           END,
       CASE LOWER(TRIM(txn_type)) WHEN 'deposit' THEN 'Deposit' WHEN 'withdrawal' THEN 'Withdrawal' END,
       CAST(REPLACE(TRIM(amount), ',', '') AS UNSIGNED),
       CAST(TRIM(commission) AS UNSIGNED)
FROM (SELECT ledger_raw.*, REPLACE(TRIM(phone), ' ', '') AS p FROM ledger_raw) AS r;
