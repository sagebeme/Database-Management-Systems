-- Create the view catalogue: title, channel, first_aired, and genres (the show's genre names, alphabetical, joined by ', '; NULL if none).
CREATE VIEW catalogue AS
SELECT s.title, s.channel, s.first_aired,
       GROUP_CONCAT(g.name ORDER BY g.name SEPARATOR ', ') AS genres
FROM tv_shows AS s
LEFT JOIN tv_show_genres AS sg ON sg.show_id = s.id
LEFT JOIN tv_genres AS g ON g.id = sg.genre_id
GROUP BY s.id, s.title, s.channel, s.first_aired;
