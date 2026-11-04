SELECT id
FROM (SELECT id, row_number() OVER (PARTITION BY rider_id, driver_id, requested_at ORDER BY id) AS n FROM trips) t
WHERE n > 1
ORDER BY id;
