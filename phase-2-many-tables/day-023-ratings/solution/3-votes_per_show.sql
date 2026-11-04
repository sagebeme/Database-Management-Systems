-- Every show and how many ratings it has, zero included: title, votes. Most first, ties alphabetical.
SELECT s.title, COUNT(r.show_id) AS votes
FROM tv_shows AS s
LEFT JOIN tv_show_ratings AS r ON r.show_id = s.id
GROUP BY s.id, s.title
ORDER BY votes DESC, s.title;
