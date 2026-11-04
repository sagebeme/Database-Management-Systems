-- Kata: Busiest Day. The single day with the biggest takings: sold_on and takings.
SELECT sold_on, SUM(qty * unit_price) AS takings
FROM sales
GROUP BY sold_on
ORDER BY takings DESC
LIMIT 1;
