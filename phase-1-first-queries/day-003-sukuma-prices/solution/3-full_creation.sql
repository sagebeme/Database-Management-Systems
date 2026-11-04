-- Create the orders table and add the four orders from the README, in one file.
CREATE TABLE IF NOT EXISTS orders (
    customer VARCHAR(50),
    item VARCHAR(50),
    qty INT
);
INSERT INTO orders (customer, item, qty) VALUES
    ('Kamau', 'Tomatoes', 2),
    ('Njeri', 'Managu', 3),
    ('Otieno', 'Avocado', 6),
    ('Njeri', 'Onions', 1);
