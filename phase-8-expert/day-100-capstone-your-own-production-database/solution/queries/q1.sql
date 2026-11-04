-- question: What does one student owe, term by term? (The bursar types an admission number.)
SELECT t.year, t.term, i.amount AS invoiced, COALESCE(sum(p.amount), 0) AS paid,
       i.amount - COALESCE(sum(p.amount), 0) AS balance
FROM students s
JOIN invoices i ON i.student_id = s.id
JOIN terms t ON t.id = i.term_id
LEFT JOIN payments p ON p.invoice_id = i.id
WHERE s.adm_no = 'ADM00077'
GROUP BY t.year, t.term, i.id, i.amount
ORDER BY t.year, t.term;
