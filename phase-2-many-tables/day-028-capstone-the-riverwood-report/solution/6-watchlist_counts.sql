-- Every show and how many times it has been saved to a watchlist, zero included. Most first, ties alphabetical.
-- Columns: title, saves
SELECT s.title, COUNT(w.id) AS saves
FROM tv_shows AS s
LEFT JOIN watchlist AS w ON w.show_id = s.id
GROUP BY s.id, s.title
ORDER BY saves DESC, s.title;
