-- id and posted of every notice about something closed or closing on a road (English full-text search:
-- "closed", "closing" and "close" all count, and so do "road" and "roads"), by id.
-- Write your statement below this line.
SELECT id, posted
FROM notices
WHERE to_tsvector('english', body) @@ to_tsquery('english', 'close & road')
ORDER BY id;
