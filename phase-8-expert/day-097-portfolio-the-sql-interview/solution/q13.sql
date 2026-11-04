SELECT driver_id, count(*) FILTER (WHERE rating < avg_rating) AS below_average
FROM (SELECT driver_id, rating, avg(rating) OVER (PARTITION BY driver_id) AS avg_rating
      FROM trips WHERE status = 'completed' AND rating IS NOT NULL) rated
GROUP BY driver_id
ORDER BY driver_id;
