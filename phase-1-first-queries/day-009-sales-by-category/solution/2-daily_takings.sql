-- Each day and the money taken that day (takings), in date order.
SELECT sold_on, SUM(qty * unit_price) AS takings FROM sales GROUP BY sold_on ORDER BY sold_on;
