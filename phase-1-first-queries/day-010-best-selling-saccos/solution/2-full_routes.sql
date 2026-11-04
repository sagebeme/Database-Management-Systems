-- Routes averaging at least 9.5 passengers a trip: route_no and avg_passengers (rounded to 1 place), fullest first.
SELECT route_no, ROUND(AVG(passengers), 1) AS avg_passengers
FROM trips
GROUP BY route_no
HAVING AVG(passengers) >= 9.5
ORDER BY AVG(passengers) DESC;
