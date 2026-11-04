-- Make an items table with one row per item: name, and price as the highest price recorded for it.
CREATE TABLE items AS
SELECT item AS name, MAX(item_price) AS price
FROM orders_flat
GROUP BY item;
