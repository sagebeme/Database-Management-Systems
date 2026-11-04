WITH firsts AS (
    SELECT rider_id, date_trunc('month', min(requested_at)) AS cohort
    FROM trips WHERE status = 'completed'
    GROUP BY rider_id
), returned AS (
    SELECT f.rider_id, f.cohort,
           EXISTS (SELECT 1 FROM trips t
                   WHERE t.rider_id = f.rider_id AND t.status = 'completed'
                     AND date_trunc('month', t.requested_at) = f.cohort + interval '1 month') AS came_back
    FROM firsts f
)
SELECT to_char(cohort, 'YYYY-MM') AS cohort, count(*) AS riders,
       count(*) FILTER (WHERE came_back) AS came_back,
       round(100.0 * count(*) FILTER (WHERE came_back) / count(*), 1) AS retention_percent
FROM returned
WHERE cohort < '2026-04-01'
GROUP BY cohort
ORDER BY cohort;
