-- Each channel's average vote across all its shows' ratings (2 places). Channels with no votes are left out. Best first, ties alphabetical.
-- Columns: channel, average
SELECT s.channel, ROUND(AVG(r.rate), 2) AS average
FROM tv_shows AS s
JOIN tv_show_ratings AS r ON r.show_id = s.id
GROUP BY s.channel
ORDER BY AVG(r.rate) DESC, s.channel;
