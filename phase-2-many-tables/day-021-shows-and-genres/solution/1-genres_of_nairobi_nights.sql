-- The genres of Nairobi Nights: name, alphabetical.
SELECT g.name
FROM tv_genres AS g
JOIN tv_show_genres AS sg ON sg.genre_id = g.id
JOIN tv_shows AS s ON s.id = sg.show_id
WHERE s.title = 'Nairobi Nights'
ORDER BY g.name;
