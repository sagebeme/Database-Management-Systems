-- A duka's stock and its orders (invented).
--   tools/mysql.sh duka < phase-5-advanced-mysql/day-058-stock-goes-down/setup.sql
DROP TABLE IF EXISTS stock_log, orders, items;
CREATE TABLE items (
    name VARCHAR(40) PRIMARY KEY,
    quantity INT NOT NULL DEFAULT 10
);
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(40) NOT NULL,
    number INT NOT NULL,
    FOREIGN KEY (item_name) REFERENCES items (name)
);
CREATE TABLE stock_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(40) NOT NULL,
    old_quantity INT NOT NULL,
    new_quantity INT NOT NULL,
    logged_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO items (name, quantity) VALUES
    ('Maize flour 2kg', 40), ('Sugar 1kg', 25), ('Cooking oil 1L', 12), ('Rice 1kg', 30), ('Milk 500ml', 18);
