-- Customers of a hardware shop in Kitale who buy on credit. Some details were never collected,
-- so they're NULL. Names and numbers are made up.
--   tools/mysql.sh hardware < phase-1-first-queries/day-011-missing-phone-numbers/setup.sql
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    id INT,
    name VARCHAR(60),
    phone VARCHAR(12),
    email VARCHAR(80),
    credit_limit DECIMAL(10, 2),
    referred_by INT
);
INSERT INTO customers (id, name, phone, email, credit_limit, referred_by) VALUES
    (1, 'Wanjiku Kamau', '254711000001', 'wanjiku@example.com', 50000.00, NULL),
    (2, 'Kiprotich Rono', NULL, 'kiprotich@example.com', 20000.00, 1),
    (3, 'Nasimiyu Wafula', '254711000003', NULL, NULL, 1),
    (4, 'Omari Hassan', NULL, NULL, 10000.00, 2),
    (5, 'Chepchumba Koech', '254711000005', NULL, 30000.00, NULL),
    (6, 'Barasa Makokha', NULL, NULL, NULL, 3),
    (7, 'Achola Owino', '254711000007', 'achola@example.com', 0.00, 2),
    (8, 'Mutiso Kilonzo', NULL, 'mutiso@example.com', NULL, NULL);
