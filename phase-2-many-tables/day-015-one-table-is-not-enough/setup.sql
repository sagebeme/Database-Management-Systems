-- Orders at a stationery shop in Nakuru, kept in one big table: every order repeats the
-- customer's details and the item's price. Names and numbers are made up.
--   tools/mysql.sh stationery < phase-2-many-tables/day-015-one-table-is-not-enough/setup.sql
DROP TABLE IF EXISTS orders_flat;
CREATE TABLE orders_flat (
    order_id INT,
    ordered_on DATE,
    customer_name VARCHAR(60),
    customer_phone VARCHAR(12),
    customer_town VARCHAR(30),
    item VARCHAR(40),
    item_price DECIMAL(8, 2),
    qty INT
);
INSERT INTO orders_flat VALUES
    (1, '2025-05-02', 'Kamau Njoroge', '254720000001', 'Nakuru', 'Exercise book', 60.00, 10),
    (2, '2025-05-02', 'Akinyi Otieno', '254720000002', 'Naivasha', 'Biro pen', 20.00, 24),
    (3, '2025-05-05', 'Kamau Njoroge', '254720000001', 'Nakuru', 'Ruler', 40.00, 5),
    (4, '2025-05-06', 'Chebet Kirui', '254720000003', 'Molo', 'Exercise book', 60.00, 30),
    (5, '2025-05-09', 'Kamau Njoroge', '254720009999', 'Nakuru', 'Geometry set', 350.00, 2),
    (6, '2025-05-12', 'Akinyi Otieno', '254720000002', 'Naivasha', 'Exercise book', 65.00, 12),
    (7, '2025-05-13', 'Chebet Kirui', '254720000003', 'Molo', 'Manila paper', 15.00, 50),
    (8, '2025-05-15', 'Kamau Njoroge', '254720000001', 'Nakuru', 'Biro pen', 20.00, 48);
