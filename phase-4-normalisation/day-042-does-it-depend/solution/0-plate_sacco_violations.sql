-- Does plate -> sacco hold? List each plate recorded with more than one sacco: plate, saccos (how many). By plate.
SELECT plate, COUNT(DISTINCT sacco) AS saccos
FROM trips
GROUP BY plate
HAVING COUNT(DISTINCT sacco) > 1
ORDER BY plate;
