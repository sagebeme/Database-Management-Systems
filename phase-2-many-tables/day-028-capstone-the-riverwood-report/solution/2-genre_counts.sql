-- Every genre and how many shows it has, zero included. Most first, ties alphabetical.
-- Columns: genre, shows
SELECT g.name AS genre, COUNT(sg.show_id) AS shows
FROM tv_genres AS g
LEFT JOIN tv_show_genres AS sg ON sg.genre_id = g.id
GROUP BY g.id, g.name
ORDER BY shows DESC, genre;
