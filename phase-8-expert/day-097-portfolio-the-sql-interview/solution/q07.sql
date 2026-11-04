SELECT day, revenue, sum(revenue) OVER (ORDER BY day) AS running_total
FROM (SELECT requested_at::date AS day, sum(fare) AS revenue
      FROM trips WHERE status = 'completed' GROUP BY 1) daily
ORDER BY day;
