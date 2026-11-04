-- Each category and the money it took (revenue), biggest first.
SELECT category, SUM(qty * unit_price) AS revenue FROM sales GROUP BY category ORDER BY revenue DESC;
