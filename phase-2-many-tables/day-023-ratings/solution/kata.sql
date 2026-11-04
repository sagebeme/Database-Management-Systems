-- Kata: Above the Average Show. Shows whose rating sum beats the average of all shows' sums: title, rating. Highest first, ties alphabetical.
SELECT s.title, SUM(r.rate) AS rating
FROM tv_shows AS s
JOIN tv_show_ratings AS r ON r.show_id = s.id
GROUP BY s.id, s.title
HAVING SUM(r.rate) > (
    SELECT AVG(total)
    FROM (SELECT SUM(rate) AS total FROM tv_show_ratings GROUP BY show_id) AS t
)
ORDER BY rating DESC, s.title;
