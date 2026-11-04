-- Every rated genre and the sum of its shows' ratings: name, rating. Highest first, ties alphabetical.
SELECT g.name, SUM(r.rate) AS rating
FROM tv_genres AS g
JOIN tv_show_genres AS sg ON sg.genre_id = g.id
JOIN tv_show_ratings AS r ON r.show_id = sg.show_id
GROUP BY g.id, g.name
ORDER BY rating DESC, g.name;
