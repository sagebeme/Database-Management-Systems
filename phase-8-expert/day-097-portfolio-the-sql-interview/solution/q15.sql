SELECT t.rider_id
FROM trips t JOIN drivers d ON d.id = t.driver_id
WHERE t.status = 'completed'
GROUP BY t.rider_id
HAVING count(DISTINCT d.vehicle) = (SELECT count(DISTINCT vehicle) FROM drivers)
ORDER BY t.rider_id;
