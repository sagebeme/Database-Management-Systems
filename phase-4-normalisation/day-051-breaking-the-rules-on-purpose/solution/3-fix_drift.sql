-- Set every shop's orders_count to its real number of orders, in one statement.
-- Write your statement below this line.
UPDATE shops AS s
SET orders_count = (SELECT COUNT(*) FROM orders AS o WHERE o.shop_id = s.id);
