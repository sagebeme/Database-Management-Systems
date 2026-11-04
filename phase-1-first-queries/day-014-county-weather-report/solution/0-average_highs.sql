-- Each county and its average daily high (avg_max, 1 decimal place), hottest first.
SELECT county, ROUND(AVG(max_c), 1) AS avg_max
FROM readings
GROUP BY county
ORDER BY AVG(max_c) DESC;
