-- For each former province: former_province, counties, population. Most people first.
SELECT former_province, COUNT(*) AS counties, SUM(population) AS population
FROM counties
GROUP BY former_province
ORDER BY population DESC;
