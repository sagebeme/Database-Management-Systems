-- A 3-day moving average: the average of this trading day and the two before it (fewer at the start),
-- rounded to a whole shilling: till, day, amount, avg3. By till, then day.
-- Write your statement below this line.
SELECT till, day, amount,
       ROUND(AVG(amount) OVER (PARTITION BY till ORDER BY day ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)) AS avg3
FROM takings
ORDER BY till, day;
