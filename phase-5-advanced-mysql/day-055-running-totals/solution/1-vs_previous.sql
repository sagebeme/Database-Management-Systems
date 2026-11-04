-- How each day compares with the till's previous trading day: till, day, amount, vs_previous (amount minus the
-- previous day's amount; NULL on the first day). By till, then day.
-- Write your statement below this line.
SELECT till, day, amount, amount - LAG(amount) OVER (PARTITION BY till ORDER BY day) AS vs_previous
FROM takings
ORDER BY till, day;
