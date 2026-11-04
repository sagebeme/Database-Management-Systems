-- Each genre that has shows and how many (number_of_shows): genre, number_of_shows. Most first, ties alphabetical.
SELECT g.name AS genre, COUNT(*) AS number_of_shows
FROM tv_genres AS g
JOIN tv_show_genres AS sg ON sg.genre_id = g.id
GROUP BY g.id, g.name
ORDER BY number_of_shows DESC, genre;
