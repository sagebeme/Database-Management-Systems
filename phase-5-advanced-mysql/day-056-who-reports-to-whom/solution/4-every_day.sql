-- Every calendar day from the first to the last day in takings, with that day's amount (0 when closed):
-- day, amount. In day order.
-- Write your statement below this line.
WITH RECURSIVE days AS (
    SELECT MIN(day) AS day FROM takings
    UNION ALL
    SELECT day + INTERVAL 1 DAY FROM days WHERE day < (SELECT MAX(day) FROM takings)
)
SELECT d.day, COALESCE(t.amount, 0) AS amount
FROM days AS d
LEFT JOIN takings AS t ON t.day = d.day
ORDER BY d.day;
