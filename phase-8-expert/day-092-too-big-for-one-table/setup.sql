-- 9,000 M-Pesa-style payments to a paybill, January to March 2026, in one ordinary table. Made up; the same
-- rows every time.
--   tools/psql.sh big -f phase-8-expert/day-092-too-big-for-one-table/setup.sql
DROP TABLE IF EXISTS payments_old;
CREATE TABLE payments_old (
    id BIGINT PRIMARY KEY,
    paid_on DATE NOT NULL,
    phone TEXT NOT NULL,
    amount INT NOT NULL
);
INSERT INTO payments_old
SELECT i, DATE '2026-01-01' + (i % 90), '2547' || lpad(((i * 7919) % 100000000)::text, 8, '0'), 50 + (i * 37) % 5000
FROM generate_series(1, 9000) AS i;
