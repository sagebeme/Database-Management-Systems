SELECT d.vehicle,
       round(percentile_cont(0.5) WITHIN GROUP (ORDER BY t.fare)::numeric, 1) AS median_fare
FROM trips t JOIN drivers d ON d.id = t.driver_id
WHERE t.status = 'completed'
GROUP BY d.vehicle
ORDER BY d.vehicle;
