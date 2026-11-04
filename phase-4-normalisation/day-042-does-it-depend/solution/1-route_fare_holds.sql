-- One row, one column, holds: 1 if route -> fare holds in trips, otherwise 0.
SELECT COUNT(*) = 0 AS holds
FROM (SELECT route FROM trips GROUP BY route HAVING COUNT(DISTINCT fare) > 1) AS broken;
