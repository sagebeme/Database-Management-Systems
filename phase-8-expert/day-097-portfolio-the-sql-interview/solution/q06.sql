WITH monthly AS (
    SELECT to_char(requested_at, 'YYYY-MM') AS month, sum(fare) AS revenue
    FROM trips WHERE status = 'completed'
    GROUP BY 1
)
SELECT month, revenue,
       round(100.0 * (revenue - lag(revenue) OVER w) / lag(revenue) OVER w, 1) AS growth
FROM monthly
WINDOW w AS (ORDER BY month)
ORDER BY month;
