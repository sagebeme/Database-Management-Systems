-- Every show with each of its genres (NULL for a show with none): title, genre. Ordered by title, then genre.
SELECT s.title, g.name AS genre
FROM tv_shows AS s
LEFT JOIN tv_show_genres AS sg ON sg.show_id = s.id
LEFT JOIN tv_genres AS g ON g.id = sg.genre_id
ORDER BY s.title, genre;
