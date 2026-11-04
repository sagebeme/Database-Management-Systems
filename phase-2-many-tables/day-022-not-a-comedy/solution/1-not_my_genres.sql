-- Genres Fundi Hacker does not have: name, alphabetical.
SELECT g.name
FROM tv_genres AS g
WHERE NOT EXISTS (
    SELECT 1
    FROM tv_show_genres AS sg
    JOIN tv_shows AS s ON s.id = sg.show_id
    WHERE sg.genre_id = g.id AND s.title = 'Fundi Hacker'
)
ORDER BY g.name;
