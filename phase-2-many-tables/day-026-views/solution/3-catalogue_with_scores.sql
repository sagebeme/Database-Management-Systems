-- Replace catalogue so it also shows each show's average (from show_scores) as a last column, average.
CREATE OR REPLACE VIEW catalogue AS
SELECT s.title, s.channel, s.first_aired,
       GROUP_CONCAT(g.name ORDER BY g.name SEPARATOR ', ') AS genres,
       sc.average
FROM tv_shows AS s
JOIN show_scores AS sc ON sc.show_id = s.id
LEFT JOIN tv_show_genres AS sg ON sg.show_id = s.id
LEFT JOIN tv_genres AS g ON g.id = sg.genre_id
GROUP BY s.id, s.title, s.channel, s.first_aired, sc.average;
