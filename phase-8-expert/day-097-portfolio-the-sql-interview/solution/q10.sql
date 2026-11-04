SELECT t.requested_at::date AS day,
       round(avg(CASE WHEN t.status = 'cancelled' THEN 1.0 ELSE 0 END), 2) AS cancellation_rate
FROM trips t JOIN riders r ON r.id = t.rider_id
WHERE NOT r.banned
  AND t.requested_at >= '2026-01-01' AND t.requested_at < '2026-01-08'
GROUP BY 1
ORDER BY 1;
