-- The shop system of a chain of six dukas (the OLTP side): shops, products and 3,000 sales in early 2026.
-- Made up; the same rows every time.
--   tools/psql.sh warehouse -f phase-8-expert/day-095-the-data-warehouse/setup.sql
DROP TABLE IF EXISTS sales, products, shops CASCADE;
CREATE TABLE shops (id INT PRIMARY KEY, name TEXT NOT NULL, county TEXT NOT NULL);
CREATE TABLE products (id INT PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL, price INT NOT NULL);
CREATE TABLE sales (
    id INT PRIMARY KEY,
    shop_id INT NOT NULL REFERENCES shops (id),
    product_id INT NOT NULL REFERENCES products (id),
    qty INT NOT NULL CHECK (qty > 0),
    sold_at TIMESTAMP NOT NULL
);
INSERT INTO shops VALUES
    (1, 'Duka la Mama Njeri', 'Nairobi'), (2, 'Kisumu Corner Shop', 'Kisumu'), (3, 'Pwani Mini Mart', 'Mombasa'),
    (4, 'Nakuru Fresh', 'Nakuru'), (5, 'Ngara Stores', 'Nairobi'), (6, 'Kibos Duka', 'Kisumu');
INSERT INTO products VALUES
    (1, 'Unga 2kg', 'Flour', 210), (2, 'Sukari 1kg', 'Sugar', 180), (3, 'Maziwa 500ml', 'Dairy', 65),
    (4, 'Mkate', 'Bakery', 70), (5, 'Chai Leaves 250g', 'Beverages', 150), (6, 'Cooking Oil 1L', 'Oils', 390),
    (7, 'Mandazi', 'Bakery', 20), (8, 'Yoghurt 250ml', 'Dairy', 90);
INSERT INTO sales
SELECT i, 1 + (i * 7) % 6, 1 + (i * 11 + i / 7) % 8, 1 + (i * 13) % 5,
       TIMESTAMP '2026-01-01 07:00' + ((i * 37) % 90) * INTERVAL '1 day' + ((i * 17) % 14) * INTERVAL '1 hour'
FROM generate_series(1, 3000) AS i;
