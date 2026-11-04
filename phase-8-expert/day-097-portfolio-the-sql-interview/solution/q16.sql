WITH days AS (
    SELECT d::date AS day FROM generate_series(date '2026-01-01', date '2026-01-31', interval '1 day') AS d
), counts AS (
    SELECT days.day, count(t.id) AS trips
    FROM days LEFT JOIN trips t ON t.requested_at::date = days.day AND t.status = 'completed'
    GROUP BY days.day
)
SELECT day, trips, round(avg(trips) OVER (ORDER BY day ROWS 6 PRECEDING), 2) AS rolling_avg
FROM counts
ORDER BY day;
