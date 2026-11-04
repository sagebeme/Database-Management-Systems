WITH marked AS (
    SELECT rider_id,
           CASE WHEN requested_at - lag(requested_at) OVER (PARTITION BY rider_id ORDER BY requested_at, id)
                     <= interval '30 minutes' THEN 0 ELSE 1 END AS new_session
    FROM trips
)
SELECT rider_id, sum(new_session) AS sessions, count(*) AS requests
FROM marked
GROUP BY rider_id
HAVING sum(new_session) < count(*)
ORDER BY rider_id;
