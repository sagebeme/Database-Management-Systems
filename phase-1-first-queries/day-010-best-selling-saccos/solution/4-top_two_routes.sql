-- Leaving out Mwananchi Shuttle, and only routes with at least 8 trips: the two routes with the most passengers. route_no and passengers, most first.
SELECT route_no, SUM(passengers) AS passengers
FROM trips
WHERE sacco <> 'Mwananchi Shuttle'
GROUP BY route_no
HAVING COUNT(*) >= 8
ORDER BY passengers DESC
LIMIT 2;
