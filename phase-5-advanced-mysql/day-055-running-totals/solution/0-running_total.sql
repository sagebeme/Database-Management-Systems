-- Each till's takings so far, day by day: till, day, amount, running_total. By till, then day.
-- Write your statement below this line.
SELECT till, day, amount, SUM(amount) OVER (PARTITION BY till ORDER BY day) AS running_total
FROM takings
ORDER BY till, day;
