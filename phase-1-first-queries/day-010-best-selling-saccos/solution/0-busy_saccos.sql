-- Saccos with at least 15 trips: sacco and trips, most first, ties alphabetical.
SELECT sacco, COUNT(*) AS trips
FROM trips
GROUP BY sacco
HAVING COUNT(*) >= 15
ORDER BY trips DESC, sacco;
