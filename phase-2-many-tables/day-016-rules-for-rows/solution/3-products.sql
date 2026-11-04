-- Create products: id numbered automatically as the primary key, name required, price required and 0 by default (DECIMAL(8, 2)).
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    price DECIMAL(8, 2) NOT NULL DEFAULT 0
);
