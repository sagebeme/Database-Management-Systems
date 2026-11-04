-- Titles of shows nobody has saved to their watchlist, alphabetical. Mind the NULL.
SELECT s.title
FROM tv_shows AS s
WHERE NOT EXISTS (SELECT 1 FROM watchlist AS w WHERE w.show_id = s.id)
ORDER BY s.title;
