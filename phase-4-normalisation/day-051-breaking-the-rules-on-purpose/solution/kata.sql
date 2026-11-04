-- Each shop's best day, from daily_sales only (don't touch orders): name, day, revenue.
-- Ties: the earlier day. Alphabetical by name.
-- Write your statement below this line.
SELECT s.name, d.day, d.revenue
FROM daily_sales AS d
JOIN shops AS s ON s.id = d.shop_id
WHERE d.day = (SELECT d2.day FROM daily_sales AS d2 WHERE d2.shop_id = d.shop_id
               ORDER BY d2.revenue DESC, d2.day LIMIT 1)
ORDER BY s.name;
