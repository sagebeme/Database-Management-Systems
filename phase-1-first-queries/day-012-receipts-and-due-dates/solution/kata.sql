-- Kata: Invoices per Month. Each month (written like 2025-01) and how many invoices were issued in it, in month order.
SELECT DATE_FORMAT(issued_on, '%Y-%m') AS month, COUNT(*) AS invoices
FROM invoices
GROUP BY month
ORDER BY month;
