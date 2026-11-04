-- Kata: for each sacco, its name as sacco and its route numbers as routes, a comma and space between them,
-- in route number order (as text: '19C' comes before '33'). Saccos with no routes too, with routes NULL.
-- By sacco.
-- Write your statement below this line.
SELECT s.name AS sacco, string_agg(r.number, ', ' ORDER BY r.number) AS routes
FROM saccos AS s
LEFT JOIN routes AS r ON r.sacco_id = s.id
GROUP BY s.name
ORDER BY s.name;
