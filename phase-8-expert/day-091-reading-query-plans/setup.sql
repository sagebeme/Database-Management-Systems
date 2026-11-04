-- 5,000 customers and 60,000 orders for an online duka, made up with generate_series. The same rows every time.
--   tools/psql.sh plans -f phase-8-expert/day-091-reading-query-plans/setup.sql
DROP TABLE IF EXISTS orders, customers;
CREATE TABLE customers (
    id INT PRIMARY KEY,
    name TEXT NOT NULL,
    county TEXT NOT NULL
);
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers (id),
    placed_on DATE NOT NULL,
    total INT NOT NULL
);
INSERT INTO customers
SELECT i, 'Customer ' || i,
       (ARRAY['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Kiambu', 'Machakos', 'Nyeri'])[1 + i % 8]
FROM generate_series(1, 5000) AS i;
INSERT INTO orders
SELECT i, 1 + (i * 7919) % 5000, DATE '2025-01-01' + (i * 13) % 365, 100 + (i * 31) % 9900
FROM generate_series(1, 60000) AS i;
ANALYZE customers, orders;
