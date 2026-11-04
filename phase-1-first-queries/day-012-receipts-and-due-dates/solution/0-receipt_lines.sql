-- One line per invoice in id order, in a column called line, like: FATMA SAID: KES 18,500.00
SELECT CONCAT(UPPER(customer), ': KES ', FORMAT(amount, 2)) AS line FROM invoices ORDER BY id;
