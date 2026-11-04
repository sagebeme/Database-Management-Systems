-- Every employee and their manager's name (NULL for nobody): employee, manager. Alphabetical by employee.
SELECT e.name AS employee, m.name AS manager
FROM employees AS e
LEFT JOIN employees AS m ON m.id = e.manager_id
ORDER BY employee;
