-- Record days: days when a till took more than on any earlier day (its first day counts):
-- till, day, amount. By till, then day.
-- Write your statement below this line.
SELECT till, day, amount
FROM (
    SELECT till, day, amount,
           MAX(amount) OVER (PARTITION BY till ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) AS best_before
    FROM takings
) AS t
WHERE best_before IS NULL OR amount > best_before
ORDER BY till, day;
