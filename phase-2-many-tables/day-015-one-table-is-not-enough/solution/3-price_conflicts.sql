-- Items recorded at more than one price: item and prices (how many different prices). Alphabetical.
SELECT item, COUNT(DISTINCT item_price) AS prices
FROM orders_flat
GROUP BY item
HAVING COUNT(DISTINCT item_price) > 1
ORDER BY item;
