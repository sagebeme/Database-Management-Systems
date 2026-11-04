-- Names of genres no show has, alphabetical. Use NOT EXISTS.
SELECT g.name
FROM tv_genres AS g
WHERE NOT EXISTS (SELECT 1 FROM tv_show_genres AS sg WHERE sg.genre_id = g.id)
ORDER BY g.name;
