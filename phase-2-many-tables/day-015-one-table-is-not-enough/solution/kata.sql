-- Kata: Lost With the Order. Items that appear in only one order (deleting that order would forget the item exists): item and order_id. Alphabetical.
SELECT item, MIN(order_id) AS order_id
FROM orders_flat
GROUP BY item
HAVING COUNT(*) = 1
ORDER BY item;
