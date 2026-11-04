-- Each artist's share of their country's fans, as a percentage rounded to 1 decimal place:
-- name, origin, fans, pct. By origin, then pct (biggest first), then name.
-- Write your statement below this line.
SELECT name, origin, fans, ROUND(100 * fans / SUM(fans) OVER (PARTITION BY origin), 1) AS pct
FROM artists
ORDER BY origin, pct DESC, name;
