-- Rated comedies and their rating sums. Highest first, ties alphabetical.
-- Columns: title, rating
SELECT s.title, SUM(r.rate) AS rating
FROM tv_shows AS s
JOIN tv_show_genres AS sg ON sg.show_id = s.id
JOIN tv_genres AS g ON g.id = sg.genre_id
JOIN tv_show_ratings AS r ON r.show_id = s.id
WHERE g.name = 'Comedy'
GROUP BY s.id, s.title
ORDER BY rating DESC, s.title;
