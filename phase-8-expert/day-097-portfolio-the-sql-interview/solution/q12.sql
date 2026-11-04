SELECT d.id AS driver_id,
       count(t.id) FILTER (WHERE t.payment = 'mpesa') AS mpesa,
       count(t.id) FILTER (WHERE t.payment = 'cash') AS cash,
       count(t.id) AS total
FROM drivers d
LEFT JOIN trips t ON t.driver_id = d.id AND t.status = 'completed'
GROUP BY d.id
ORDER BY d.id;
