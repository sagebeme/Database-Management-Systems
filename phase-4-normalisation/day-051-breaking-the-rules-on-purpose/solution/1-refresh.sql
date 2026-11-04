-- Bring daily_sales up to date with orders. It must be safe to run again and again: after new orders, after
-- none, after an order is deleted.
-- Write your statement below this line.
DELETE FROM daily_sales;
INSERT INTO daily_sales
SELECT shop_id, placed_on, COUNT(*), SUM(total) FROM orders GROUP BY shop_id, placed_on;
