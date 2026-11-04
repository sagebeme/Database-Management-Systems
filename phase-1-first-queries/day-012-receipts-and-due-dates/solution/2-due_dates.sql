-- Each invoice's id and the date it is due (due_on): issued_on plus days_to_pay days. In id order.
SELECT id, DATE_ADD(issued_on, INTERVAL days_to_pay DAY) AS due_on FROM invoices ORDER BY id;
