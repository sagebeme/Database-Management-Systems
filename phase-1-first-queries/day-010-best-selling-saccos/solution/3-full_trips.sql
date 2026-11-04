-- Count each sacco's trips with 10 or more passengers (full_trips), and keep saccos with at least 10 such trips. Alphabetical by sacco.
SELECT sacco, COUNT(*) AS full_trips
FROM trips
WHERE passengers >= 10
GROUP BY sacco
HAVING COUNT(*) >= 10
ORDER BY sacco;
