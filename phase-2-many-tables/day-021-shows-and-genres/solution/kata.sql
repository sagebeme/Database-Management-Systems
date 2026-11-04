-- Kata: Romance and Drama. Titles of shows that are both Drama and Romance, alphabetical.
SELECT s.title
FROM tv_shows AS s
JOIN tv_show_genres AS sg ON sg.show_id = s.id
JOIN tv_genres AS g ON g.id = sg.genre_id
WHERE g.name IN ('Drama', 'Romance')
GROUP BY s.id, s.title
HAVING COUNT(DISTINCT g.name) = 2
ORDER BY s.title;
