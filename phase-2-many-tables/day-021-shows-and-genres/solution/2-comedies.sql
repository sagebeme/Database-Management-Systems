-- Titles of every comedy, alphabetical.
SELECT s.title
FROM tv_shows AS s
JOIN tv_show_genres AS sg ON sg.show_id = s.id
JOIN tv_genres AS g ON g.id = sg.genre_id
WHERE g.name = 'Comedy'
ORDER BY s.title;
