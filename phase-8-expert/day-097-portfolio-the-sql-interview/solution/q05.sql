WITH days AS (
    SELECT DISTINCT driver_id, requested_at::date AS day
    FROM trips WHERE status = 'completed'
), islands AS (
    SELECT driver_id, day,
           day - (row_number() OVER (PARTITION BY driver_id ORDER BY day))::integer AS island
    FROM days
)
SELECT driver_id, min(day) AS first_day, max(day) AS last_day, count(*) AS days
FROM islands
GROUP BY driver_id, island
HAVING count(*) >= 3
ORDER BY driver_id, first_day;
