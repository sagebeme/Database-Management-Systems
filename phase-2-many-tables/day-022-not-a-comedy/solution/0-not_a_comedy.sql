-- Titles of every show that is not a comedy (shows with no genre count), alphabetical.
SELECT title
FROM tv_shows
WHERE id NOT IN (
    SELECT sg.show_id
    FROM tv_show_genres AS sg
    JOIN tv_genres AS g ON g.id = sg.genre_id
    WHERE g.name = 'Comedy'
)
ORDER BY title;
