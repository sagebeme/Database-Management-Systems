-- Days followed by a drop of more than 30% on the till's next trading day:
-- till, day, amount, next_amount. By till, then day.
-- Write your statement below this line.
SELECT till, day, amount, next_amount
FROM (
    SELECT till, day, amount, LEAD(amount) OVER (PARTITION BY till ORDER BY day) AS next_amount
    FROM takings
) AS t
WHERE next_amount < amount * 0.7
ORDER BY till, day;
