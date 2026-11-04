-- Faith's M-Pesa statement for a few weeks of 2025. Codes, names and amounts are made up.
--   tools/mysql.sh mpesa < phase-1-first-queries/day-005-mpesa-search/setup.sql
DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions (
    code CHAR(10),
    kind VARCHAR(10),
    counterparty VARCHAR(60),
    amount DECIMAL(10, 2),
    happened_at DATETIME
);
INSERT INTO transactions (code, kind, counterparty, amount, happened_at) VALUES
    ('TB21KQ8XZ1', 'Received', 'Peter Mwangi', 5000.00, '2025-02-27 09:15:00'),
    ('TB28LM3PA2', 'Paybill', 'KPLC PREPAID', 1500.00, '2025-02-28 19:40:00'),
    ('TC01AB4QR3', 'Sent', 'Mary Achieng', 1200.00, '2025-03-01 00:05:00'),
    ('TC03XY7WE4', 'Airtime', 'Safaricom', 100.00, '2025-03-03 08:00:00'),
    ('TC05GH2TY5', 'Till', 'Naivas Ruaka', 3450.00, '2025-03-05 17:22:00'),
    ('TC09JK6UI6', 'Sent', 'Kevin Otieno', 800.00, '2025-03-09 12:10:00'),
    ('TC12ZX5CV7', 'Received', 'Grace Wambui', 500.00, '2025-03-12 14:45:00'),
    ('TC15QW9ER8', 'Paybill', 'KPLC POSTPAID', 2300.00, '2025-03-15 10:30:00'),
    ('TC18AS1DF9', 'Withdraw', 'Agent 104552', 2000.00, '2025-03-18 16:00:00'),
    ('TC20PO4IU0', 'Airtime', 'Safaricom', 20.00, '2025-03-20 21:15:00'),
    ('TC24LK8JH1', 'Sent', 'Mary Achieng', 2500.00, '2025-03-24 07:55:00'),
    ('TC27MN3BV2', 'Till', 'Java House', 640.00, '2025-03-27 13:05:00'),
    ('TC31CX6ZA3', 'Received', 'Peter Mwangi', 4200.00, '2025-03-31 18:20:00'),
    ('TD01QA2WS4', 'Paybill', 'Zuku Fibre', 2999.00, '2025-04-01 00:00:00');
