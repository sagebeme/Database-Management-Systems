-- Shows nobody has rated yet. Alphabetical.
-- Columns: title
SELECT s.title
FROM tv_shows AS s
LEFT JOIN tv_show_ratings AS r ON r.show_id = s.id
WHERE r.show_id IS NULL
ORDER BY s.title;
