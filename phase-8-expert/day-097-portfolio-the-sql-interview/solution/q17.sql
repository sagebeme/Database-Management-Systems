SELECT DISTINCT ON (month) month, hour, requests
FROM (SELECT to_char(requested_at, 'YYYY-MM') AS month, extract(hour FROM requested_at)::integer AS hour,
             count(*) AS requests
      FROM trips GROUP BY 1, 2) hourly
ORDER BY month, requests DESC, hour;
