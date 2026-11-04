-- Using the show_scores view: the 3 best shows by average among those with at least 5 votes: title, average. Ties alphabetical.
SELECT title, average
FROM show_scores
WHERE votes >= 5
ORDER BY average DESC, title
LIMIT 3;
