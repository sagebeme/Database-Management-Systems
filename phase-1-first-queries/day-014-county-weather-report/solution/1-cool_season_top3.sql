-- The three counties with the highest average high in July and August: county and avg_max (1 place), hottest first.
SELECT county, ROUND(AVG(max_c), 1) AS avg_max
FROM readings
WHERE recorded_on >= '2024-07-01' AND recorded_on < '2024-09-01'
GROUP BY county
ORDER BY AVG(max_c) DESC
LIMIT 3;
