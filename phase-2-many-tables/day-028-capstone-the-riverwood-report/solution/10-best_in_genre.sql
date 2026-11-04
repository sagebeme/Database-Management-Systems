-- For each genre with rated shows, the show with the highest rating sum (all of them on a tie). Ordered by genre, then title.
-- Columns: genre, title, rating
SELECT g.name AS genre, s.title, t.rating
FROM tv_genres AS g
JOIN tv_show_genres AS sg ON sg.genre_id = g.id
JOIN tv_shows AS s ON s.id = sg.show_id
JOIN (SELECT show_id, SUM(rate) AS rating FROM tv_show_ratings GROUP BY show_id) AS t ON t.show_id = s.id
WHERE t.rating = (
    SELECT MAX(t2.rating)
    FROM tv_show_genres AS sg2
    JOIN (SELECT show_id, SUM(rate) AS rating FROM tv_show_ratings GROUP BY show_id) AS t2 ON t2.show_id = sg2.show_id
    WHERE sg2.genre_id = g.id
)
ORDER BY genre, s.title;
