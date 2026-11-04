-- Each channel and how many shows it has. Alphabetical.
-- Columns: channel, shows
SELECT channel, COUNT(*) AS shows
FROM tv_shows
GROUP BY channel
ORDER BY channel;
