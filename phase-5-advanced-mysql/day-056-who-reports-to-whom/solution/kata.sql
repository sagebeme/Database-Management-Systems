-- The lowest common boss of Brian Kiprono and Samuel Mutua: the closest person both of them report to,
-- directly or not (someone counts as reporting to themselves). name.
-- Write your statement below this line.
WITH RECURSIVE up AS (
    SELECT name AS who, id, manager_id, 0 AS steps
    FROM employees
    WHERE name IN ('Brian Kiprono', 'Samuel Mutua')
    UNION ALL
    SELECT u.who, e.id, e.manager_id, u.steps + 1
    FROM up AS u
    JOIN employees AS e ON e.id = u.manager_id
)
SELECT e.name
FROM up AS a
JOIN up AS b ON b.id = a.id AND a.who = 'Brian Kiprono' AND b.who = 'Samuel Mutua'
JOIN employees AS e ON e.id = a.id
ORDER BY a.steps
LIMIT 1;
