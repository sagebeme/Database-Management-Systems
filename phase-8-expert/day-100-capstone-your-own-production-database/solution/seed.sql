-- Made-up data, big enough that the planner has to choose: 400 guardians, 600 students,
-- 6 terms, 3,600 invoices and about 12,000 payments.

INSERT INTO guardians (name, phone)
SELECT (ARRAY['Wanjiru', 'Otieno', 'Akinyi', 'Kiprop', 'Mwende', 'Baraka', 'Nafula', 'Hassan'])[1 + i % 8] || ' ' ||
       (ARRAY['Kamau', 'Ochieng', 'Mutua', 'Chebet', 'Njoroge', 'Wekesa', 'Ali'])[1 + i % 7],
       '2547' || lpad((i * 1931)::text, 8, '0')
FROM generate_series(1, 400) AS i;

INSERT INTO students (adm_no, name, guardian_id, class)
SELECT 'ADM' || lpad(i::text, 5, '0'),
       (ARRAY['Imani', 'Baraka', 'Zawadi', 'Jabali', 'Neema', 'Tumaini', 'Amani'])[1 + i % 7] || ' ' ||
       (ARRAY['Kamau', 'Ochieng', 'Mutua', 'Chebet', 'Njoroge', 'Wekesa', 'Ali'])[1 + (i / 7) % 7],
       1 + (i * 7) % 400,
       (ARRAY['Grade 7', 'Grade 8', 'Grade 9', 'Form 3', 'Form 4'])[1 + i % 5]
FROM generate_series(1, 600) AS i;

INSERT INTO terms (year, term, starts_on, ends_on)
SELECT y, t, make_date(y, (t - 1) * 4 + 1, 6), make_date(y, (t - 1) * 4 + 4, 4)
FROM generate_series(2025, 2026) AS y, generate_series(1, 3) AS t;

INSERT INTO invoices (student_id, term_id, amount)
SELECT s.id, t.id, CASE WHEN s.class LIKE 'Form%' THEN 18500 ELSE 12000 END
FROM students s CROSS JOIN terms t;

-- Most families pay in instalments; some fall behind.
INSERT INTO payments (invoice_id, mpesa_receipt, amount, paid_at)
SELECT i.id,
       upper(substr(md5(i.id::text || '-' || n), 1, 10)),
       i.amount / 4,
       t.starts_on + (n * 17 + i.id % 9) * interval '1 day' + (i.id % 600) * interval '1 minute'
FROM invoices i
JOIN terms t ON t.id = i.term_id
CROSS JOIN generate_series(1, 4) AS n
WHERE n <= 4 - (i.student_id % 7 = 0)::integer - (i.student_id % 11 = 0)::integer * 2;

ANALYZE;
