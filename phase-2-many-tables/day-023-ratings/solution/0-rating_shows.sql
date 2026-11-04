-- Every rated show and the sum of its ratings: title, rating. Highest first, ties alphabetical.
SELECT s.title, SUM(r.rate) AS rating
FROM tv_shows AS s
JOIN tv_show_ratings AS r ON r.show_id = s.id
GROUP BY s.id, s.title
ORDER BY rating DESC, s.title;
