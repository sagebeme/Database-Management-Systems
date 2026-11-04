-- First, an index idx_placed_on on orders.placed_on. Then the number of orders and the total taken in June 2025
-- (orders, takings), written so that the index can be used.
-- Write your statement below this line.
CREATE INDEX idx_placed_on ON orders (placed_on);
SELECT COUNT(*) AS orders, SUM(total) AS takings
FROM orders
WHERE placed_on >= '2025-06-01' AND placed_on < '2025-07-01';
