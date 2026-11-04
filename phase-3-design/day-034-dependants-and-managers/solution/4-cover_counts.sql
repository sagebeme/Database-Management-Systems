-- Every employee and how many dependants their cover includes, zero included: employee, dependants. Most first, ties alphabetical.
SELECT e.name AS employee, COUNT(d.employee_id) AS dependants
FROM employees AS e
LEFT JOIN dependants AS d ON d.employee_id = e.id
GROUP BY e.id, e.name
ORDER BY dependants DESC, employee;
