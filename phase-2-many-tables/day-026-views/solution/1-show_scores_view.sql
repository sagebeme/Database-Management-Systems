-- Create the view show_scores: show_id, title, votes (0 if none) and average (rounded to 2 places; NULL if no votes) for every show.
CREATE VIEW show_scores AS
SELECT s.id AS show_id, s.title, COUNT(r.show_id) AS votes, ROUND(AVG(r.rate), 2) AS average
FROM tv_shows AS s
LEFT JOIN tv_show_ratings AS r ON r.show_id = s.id
GROUP BY s.id, s.title;
