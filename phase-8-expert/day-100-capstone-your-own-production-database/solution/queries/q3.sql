-- question: Which guardians still owe more than 5,000 for Term 1 of 2026? (For the reminder SMS.)
-- full scan: a report over every Term 1 invoice; it reads most of the table anyway.
SELECT g.name, g.phone, sum(i.amount - COALESCE(paid.total, 0)) AS owed
FROM invoices i
JOIN terms t ON t.id = i.term_id AND t.year = 2026 AND t.term = 1
JOIN students s ON s.id = i.student_id
JOIN guardians g ON g.id = s.guardian_id
LEFT JOIN (SELECT invoice_id, sum(amount) AS total FROM payments GROUP BY invoice_id) paid
       ON paid.invoice_id = i.id
GROUP BY g.id, g.name, g.phone
HAVING sum(i.amount - COALESCE(paid.total, 0)) > 5000
ORDER BY owed DESC, g.name;
