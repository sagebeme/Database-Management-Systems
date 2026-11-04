-- For invoices paid after their due date: id and how many days late (days_late), latest first.
SELECT id, DATEDIFF(paid_on, DATE_ADD(issued_on, INTERVAL days_to_pay DAY)) AS days_late
FROM invoices
WHERE paid_on > DATE_ADD(issued_on, INTERVAL days_to_pay DAY)
ORDER BY days_late DESC;
