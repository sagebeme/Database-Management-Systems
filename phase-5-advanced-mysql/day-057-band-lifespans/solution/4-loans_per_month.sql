-- How many loans started in each month: month (like 2026-01), loans. In month order.
-- Write your statement below this line.
SELECT DATE_FORMAT(borrowed_on, '%Y-%m') AS month, COUNT(*) AS loans
FROM loans
GROUP BY month
ORDER BY month;
