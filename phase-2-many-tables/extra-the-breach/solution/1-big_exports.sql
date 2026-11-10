-- Clue 1. Every export of the customers table with more than 1,000 rows: id, username, at, row_count, oldest first.
SELECT id, username, at, row_count
FROM exports
WHERE table_name = 'customers' AND row_count > 1000
ORDER BY at;
