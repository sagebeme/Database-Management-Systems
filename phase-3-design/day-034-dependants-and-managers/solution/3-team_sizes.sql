-- Each manager and how many people report to them directly: manager, reports. Most first, ties alphabetical.
SELECT m.name AS manager, COUNT(*) AS reports
FROM employees AS m
JOIN employees AS e ON e.manager_id = m.id
GROUP BY m.id, m.name
ORDER BY reports DESC, manager;
