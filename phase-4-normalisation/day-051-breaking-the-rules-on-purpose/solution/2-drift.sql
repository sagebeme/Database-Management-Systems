-- Shops whose stored orders_count doesn't match their real number of orders: name, stored_count, actual_count.
-- Alphabetical by name.
-- Write your statement below this line.
SELECT s.name, s.orders_count AS stored_count, COUNT(o.id) AS actual_count
FROM shops AS s
LEFT JOIN orders AS o ON o.shop_id = s.id
GROUP BY s.id, s.name, s.orders_count
HAVING stored_count <> actual_count
ORDER BY s.name;
