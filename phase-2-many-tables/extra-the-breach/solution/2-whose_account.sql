-- Clue 2. The same big customers exports, with whose account made each one: export id, username, the staff member's
-- name and their left_on, oldest export first. Keep exports by accounts that aren't in staff (their name and left_on
-- come back NULL).
SELECT e.id, e.username, s.name, s.left_on
FROM exports AS e
LEFT JOIN staff AS s ON s.username = e.username
WHERE e.table_name = 'customers' AND e.row_count > 1000
ORDER BY e.at;
