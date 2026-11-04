-- Kata: Shared Routes. Routes run by more than one sacco: route_no and saccos (how many), in route order.
SELECT route_no, COUNT(DISTINCT sacco) AS saccos
FROM trips
GROUP BY route_no
HAVING COUNT(DISTINCT sacco) > 1
ORDER BY route_no;
