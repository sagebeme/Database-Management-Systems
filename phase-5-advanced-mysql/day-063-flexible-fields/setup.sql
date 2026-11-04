-- A duka's catalogue (invented products). Phones, shoes and food each have their own details, kept in one JSON
-- column instead of a column for every detail any product might have.
--   tools/mysql.sh catalogue < phase-5-advanced-mysql/day-063-flexible-fields/setup.sql
DROP TABLE IF EXISTS products;
CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    category VARCHAR(20) NOT NULL,
    price INT NOT NULL,
    attributes JSON NOT NULL
);
INSERT INTO products VALUES
    (1, 'Simu Poa A1', 'phone', 8999, '{"ram_gb": 3, "storage_gb": 32, "tags": ["budget"]}'),
    (2, 'Simu Poa A5', 'phone', 15999, '{"ram_gb": 4, "storage_gb": 64, "tags": ["new"]}'),
    (3, 'Simu Poa X', 'phone', 32999, '{"ram_gb": 8, "storage_gb": 256, "dual_sim": true, "tags": ["new", "premium"]}'),
    (4, 'Simu Poa A3', 'phone', 11999, '{"ram_gb": 4, "storage_gb": 128, "tags": []}'),
    (5, 'Kitenge shirt', 'clothing', 1500, '{"size": "L", "colour": "red", "tags": ["handmade"]}'),
    (6, 'Maasai sandals', 'shoes', 1200, '{"size": 42, "colour": "brown", "tags": ["handmade", "new"]}'),
    (7, 'School shoes', 'shoes', 2500, '{"size": 38, "colour": "black", "tags": []}'),
    (8, 'Maize flour 2kg', 'food', 230, '{"weight_g": 2000, "expires": "2026-09-30", "tags": ["staple"]}'),
    (9, 'Sukuma wiki bunch', 'food', 30, '{"weight_g": 250, "tags": ["fresh", "staple"]}'),
    (10, 'Solar lamp', 'electronics', 2200, '{"watts": 5, "tags": ["new"]}');
