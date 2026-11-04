-- question: A parent reads out an M-Pesa receipt. Which student and term did it pay for?
SELECT p.mpesa_receipt, p.amount, p.paid_at, s.adm_no, s.name, t.year, t.term
FROM payments p
JOIN invoices i ON i.id = p.invoice_id
JOIN students s ON s.id = i.student_id
JOIN terms t ON t.id = i.term_id
WHERE p.mpesa_receipt = (SELECT mpesa_receipt FROM payments ORDER BY id OFFSET 500 LIMIT 1);
