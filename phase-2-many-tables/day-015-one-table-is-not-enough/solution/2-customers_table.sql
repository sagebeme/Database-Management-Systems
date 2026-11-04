-- Make a customers table with one row per customer: name, phone, town (from orders_flat, after the fix).
CREATE TABLE customers AS
SELECT DISTINCT customer_name AS name, customer_phone AS phone, customer_town AS town
FROM orders_flat;
