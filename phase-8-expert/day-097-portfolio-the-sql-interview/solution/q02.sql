SELECT driver_id, trip_id, fare
FROM (SELECT driver_id, id AS trip_id, fare,
             rank() OVER (PARTITION BY driver_id ORDER BY fare DESC) AS r
      FROM trips WHERE status = 'completed') ranked
WHERE r <= 3
ORDER BY driver_id, fare DESC, trip_id;
