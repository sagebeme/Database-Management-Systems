-- Every show with its genres (alphabetical, joined by ', '; NULL if none). Alphabetical by title.
-- Columns: title, genres
SELECT s.title, GROUP_CONCAT(g.name ORDER BY g.name SEPARATOR ', ') AS genres
FROM tv_shows AS s
LEFT JOIN tv_show_genres AS sg ON sg.show_id = s.id
LEFT JOIN tv_genres AS g ON g.id = sg.genre_id
GROUP BY s.id, s.title
ORDER BY s.title;
