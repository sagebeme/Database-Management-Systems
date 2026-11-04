-- question: How much has each class paid towards Term 1 of 2026, and what share of its fees is that?
-- full scan: a report over a whole term's payments.
SELECT s.class, sum(i.amount) AS invoiced, sum(COALESCE(paid.total, 0)) AS paid,
       round(100.0 * sum(COALESCE(paid.total, 0)) / sum(i.amount), 1) AS percent_paid
FROM invoices i
JOIN terms t ON t.id = i.term_id AND t.year = 2026 AND t.term = 1
JOIN students s ON s.id = i.student_id
LEFT JOIN (SELECT invoice_id, sum(amount) AS total FROM payments GROUP BY invoice_id) paid
       ON paid.invoice_id = i.id
GROUP BY s.class
ORDER BY s.class;
