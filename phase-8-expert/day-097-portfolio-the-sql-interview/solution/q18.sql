SELECT rank, driver_id, earnings
FROM (SELECT driver_id, sum(fare) AS earnings, dense_rank() OVER (ORDER BY sum(fare) DESC) AS rank
      FROM trips WHERE status = 'completed' GROUP BY driver_id) ranked
WHERE rank <= 3
ORDER BY rank, driver_id;
