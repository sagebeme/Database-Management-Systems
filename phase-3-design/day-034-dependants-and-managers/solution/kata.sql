-- Kata: The Boss's Boss. Each employee whose manager has a manager too, with that person: employee, grand_manager. Alphabetical by employee.
SELECT e.name AS employee, g.name AS grand_manager
FROM employees AS e
JOIN employees AS m ON m.id = e.manager_id
JOIN employees AS g ON g.id = m.manager_id
ORDER BY employee;
