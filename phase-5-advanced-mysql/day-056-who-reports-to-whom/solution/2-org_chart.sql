-- Everyone, with depth (the top person is 0) and path: the names from the top down to them, joined with ' > '.
-- name, depth, path. Ordered by path.
-- Write your statement below this line.
WITH RECURSIVE tree AS (
    SELECT id, name, 0 AS depth, CAST(name AS CHAR(1000)) AS path
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, t.depth + 1, CONCAT(t.path, ' > ', e.name)
    FROM employees AS e
    JOIN tree AS t ON e.manager_id = t.id
)
SELECT name, depth, path FROM tree ORDER BY path;
