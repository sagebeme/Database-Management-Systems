-- Shows with at least 5 ratings: title, average (rounded to 2 places), votes. Best average first, ties alphabetical.
SELECT s.title, ROUND(AVG(r.rate), 2) AS average, COUNT(*) AS votes
FROM tv_shows AS s
JOIN tv_show_ratings AS r ON r.show_id = s.id
GROUP BY s.id, s.title
HAVING COUNT(*) >= 5
ORDER BY AVG(r.rate) DESC, s.title;
