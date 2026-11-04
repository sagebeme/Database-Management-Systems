-- Brian Kiprono's chain of command, from himself (level 0) up to the top: level, name, title. By level.
-- Write your statement below this line.
WITH RECURSIVE chain AS (
    SELECT id, name, title, manager_id, 0 AS level
    FROM employees
    WHERE name = 'Brian Kiprono'
    UNION ALL
    SELECT e.id, e.name, e.title, e.manager_id, c.level + 1
    FROM employees AS e
    JOIN chain AS c ON e.id = c.manager_id
)
SELECT level, name, title FROM chain ORDER BY level;
