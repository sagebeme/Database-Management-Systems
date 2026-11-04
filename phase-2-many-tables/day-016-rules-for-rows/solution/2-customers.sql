-- Create customers (id INT, name VARCHAR(100), phone VARCHAR(12)) where no two customers can share a phone number.
CREATE TABLE IF NOT EXISTS customers (
    id INT,
    name VARCHAR(100),
    phone VARCHAR(12) UNIQUE
);
