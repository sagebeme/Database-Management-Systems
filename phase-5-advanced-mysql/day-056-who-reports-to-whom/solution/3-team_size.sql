-- Everyone who has people under them (at any depth): name, team_size. Biggest first, ties by name.
-- Write your statement below this line.
WITH RECURSIVE under AS (
    SELECT manager_id AS boss, id AS person
    FROM employees
    WHERE manager_id IS NOT NULL
    UNION ALL
    SELECT e.manager_id, u.person
    FROM under AS u
    JOIN employees AS e ON e.id = u.boss
    WHERE e.manager_id IS NOT NULL
)
SELECT b.name, COUNT(*) AS team_size
FROM under AS u
JOIN employees AS b ON b.id = u.boss
GROUP BY b.id, b.name
ORDER BY team_size DESC, b.name;
