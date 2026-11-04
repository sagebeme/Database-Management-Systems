-- The genres of the shows on akinyi's watchlist, each once. Alphabetical.
-- Columns: genre
SELECT DISTINCT g.name AS genre
FROM watchlist AS w
JOIN tv_show_genres AS sg ON sg.show_id = w.show_id
JOIN tv_genres AS g ON g.id = sg.genre_id
WHERE w.viewer = 'akinyi'
ORDER BY genre;
