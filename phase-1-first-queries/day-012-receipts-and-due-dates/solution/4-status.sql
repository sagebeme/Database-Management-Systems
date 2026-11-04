-- Each invoice's id and its status: unpaid, late, or on time. In id order.
SELECT id,
       CASE
           WHEN paid_on IS NULL THEN 'unpaid'
           WHEN paid_on > DATE_ADD(issued_on, INTERVAL days_to_pay DAY) THEN 'late'
           ELSE 'on time'
       END AS status
FROM invoices
ORDER BY id;
