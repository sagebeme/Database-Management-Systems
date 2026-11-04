-- Saccos that took more than 10,000 bob (passengers times fare, added up): sacco and revenue, biggest first.
SELECT sacco, SUM(passengers * fare_kes) AS revenue
FROM trips
GROUP BY sacco
HAVING SUM(passengers * fare_kes) > 10000
ORDER BY revenue DESC;
