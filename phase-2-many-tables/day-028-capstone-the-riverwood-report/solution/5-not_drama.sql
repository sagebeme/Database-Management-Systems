-- Shows that are not dramas, shows with no genre included. Alphabetical.
-- Columns: title
SELECT s.title
FROM tv_shows AS s
WHERE NOT EXISTS (
    SELECT 1
    FROM tv_show_genres AS sg
    JOIN tv_genres AS g ON g.id = sg.genre_id
    WHERE sg.show_id = s.id AND g.name = 'Drama'
)
ORDER BY s.title;
