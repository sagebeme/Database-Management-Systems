-- The three wettest months across all counties: month (like 2024-05) and rain (total mm), wettest first.
SELECT DATE_FORMAT(recorded_on, '%Y-%m') AS month, SUM(rain_mm) AS rain
FROM readings
GROUP BY month
ORDER BY rain DESC
LIMIT 3;
