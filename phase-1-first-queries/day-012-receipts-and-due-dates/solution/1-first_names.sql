-- Each invoice's id and the customer's first name (first_name), in id order.
SELECT id, SUBSTRING_INDEX(customer, ' ', 1) AS first_name FROM invoices ORDER BY id;
