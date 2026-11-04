-- Kata: The Genre Board. Create the view genre_board: genre, shows, votes, average (2 places) for every genre, including genres with no shows (0, 0, NULL).
CREATE VIEW genre_board AS
SELECT g.name AS genre,
       COUNT(DISTINCT sg.show_id) AS shows,
       COUNT(r.show_id) AS votes,
       ROUND(AVG(r.rate), 2) AS average
FROM tv_genres AS g
LEFT JOIN tv_show_genres AS sg ON sg.genre_id = g.id
LEFT JOIN tv_show_ratings AS r ON r.show_id = sg.show_id
GROUP BY g.id, g.name;
