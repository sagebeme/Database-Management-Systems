-- A delivery app's shops and orders (invented). shops.orders_count is a copy of a number you could count,
-- kept so the shop list loads fast. Somebody's code forgot to update it a few times.
--   tools/mysql.sh dukas < phase-4-normalisation/day-051-breaking-the-rules-on-purpose/setup.sql
DROP TABLE IF EXISTS daily_sales, orders, shops;
CREATE TABLE shops (
    id INT PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    orders_count INT NOT NULL DEFAULT 0
);
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    shop_id INT NOT NULL,
    placed_on DATE NOT NULL,
    total INT NOT NULL,
    FOREIGN KEY (shop_id) REFERENCES shops (id)
);
INSERT INTO shops VALUES
    (1, 'Kawangware Fresh', 8),
    (2, 'Mama Njeri Groceries', 13),
    (3, 'Ongata Rongai Mart', 2),
    (4, 'Thika Road Duka', 6);
INSERT INTO orders VALUES
    (1, 1, '2026-03-06', 3650),
    (2, 1, '2026-03-03', 1600),
    (3, 4, '2026-03-06', 1750),
    (4, 4, '2026-03-05', 3650),
    (5, 2, '2026-03-06', 3500),
    (6, 3, '2026-03-04', 3900),
    (7, 3, '2026-03-04', 2600),
    (8, 2, '2026-03-05', 150),
    (9, 4, '2026-03-02', 300),
    (10, 2, '2026-03-04', 350),
    (11, 2, '2026-03-03', 2350),
    (12, 2, '2026-03-04', 2500),
    (13, 2, '2026-03-03', 300),
    (14, 2, '2026-03-03', 3150),
    (15, 1, '2026-03-02', 800),
    (16, 4, '2026-03-06', 800),
    (17, 1, '2026-03-06', 3100),
    (18, 1, '2026-03-05', 2800),
    (19, 1, '2026-03-04', 850),
    (20, 2, '2026-03-06', 1250),
    (21, 2, '2026-03-04', 3000),
    (22, 2, '2026-03-02', 3450),
    (23, 4, '2026-03-05', 200),
    (24, 2, '2026-03-06', 400),
    (25, 2, '2026-03-06', 3600),
    (26, 1, '2026-03-06', 2100),
    (27, 2, '2026-03-05', 300),
    (28, 2, '2026-03-05', 3500),
    (29, 1, '2026-03-06', 3850),
    (30, 2, '2026-03-06', 1900);
