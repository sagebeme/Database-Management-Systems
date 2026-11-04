-- Titles viewers saved that Riverwood doesn't carry, with how many times each was asked for. Most first, ties alphabetical.
-- Columns: requested_title, requests
SELECT requested_title, COUNT(*) AS requests
FROM watchlist
WHERE show_id IS NULL
GROUP BY requested_title
ORDER BY requests DESC, requested_title;
