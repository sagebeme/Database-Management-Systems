-- Employees with no manager: name, alphabetical.
SELECT name
FROM employees
WHERE manager_id IS NULL
ORDER BY name;
