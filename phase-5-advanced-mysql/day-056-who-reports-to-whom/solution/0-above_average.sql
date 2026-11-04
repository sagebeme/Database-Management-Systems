-- With a CTE (WITH ... AS): people paid more than their department's average: name, department, salary,
-- dept_avg (rounded to a whole shilling). By department, then salary (highest first).
-- Write your statement below this line.
WITH averages AS (
    SELECT department, AVG(salary) AS dept_avg
    FROM employees
    GROUP BY department
)
SELECT e.name, e.department, e.salary, ROUND(a.dept_avg) AS dept_avg
FROM employees AS e
JOIN averages AS a ON a.department = e.department
WHERE e.salary > a.dept_avg
ORDER BY e.department, e.salary DESC;
