-- Genres whose ratings average above the average of all ratings: genre, average (2 places). Best first, ties alphabetical.
SELECT g.name AS genre, ROUND(AVG(r.rate), 2) AS average
FROM tv_genres AS g
JOIN tv_show_genres AS sg ON sg.genre_id = g.id
JOIN tv_show_ratings AS r ON r.show_id = sg.show_id
GROUP BY g.id, g.name
HAVING AVG(r.rate) > (SELECT AVG(rate) FROM tv_show_ratings)
ORDER BY AVG(r.rate) DESC, genre;
