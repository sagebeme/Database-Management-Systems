-- Titles of shows with no genre at all, alphabetical. Use a LEFT JOIN.
SELECT s.title
FROM tv_shows AS s
LEFT JOIN tv_show_genres AS sg ON sg.show_id = s.id
WHERE sg.show_id IS NULL
ORDER BY s.title;
