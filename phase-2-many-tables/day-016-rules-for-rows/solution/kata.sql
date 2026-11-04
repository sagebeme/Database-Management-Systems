-- Kata: Which Id? Insert a product called Kalamu priced 25, then print the id MySQL gave it in a column called new_id. Don't type the number.
INSERT INTO products (name, price) VALUES ('Kalamu', 25);
SELECT LAST_INSERT_ID() AS new_id;
