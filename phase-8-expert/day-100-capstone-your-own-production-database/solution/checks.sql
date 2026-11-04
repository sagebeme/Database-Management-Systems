-- Each statement below must be refused by the database itself.

-- expect error: a phone number without the country code
INSERT INTO guardians (name, phone) VALUES ('Test Parent', '0712345678');

-- expect error: a student with a guardian who doesn't exist
INSERT INTO students (adm_no, name, guardian_id, class) VALUES ('ADM99999', 'Ghost', 999999, 'Grade 7');

-- expect error: the same M-Pesa receipt recorded twice
INSERT INTO payments (invoice_id, mpesa_receipt, amount, paid_at)
SELECT invoice_id, mpesa_receipt, amount, paid_at FROM payments LIMIT 1;

-- expect error: a negative payment
INSERT INTO payments (invoice_id, mpesa_receipt, amount, paid_at) VALUES (1, 'ABCDE12345', -500, now());

-- expect error: two invoices for one student in one term
INSERT INTO invoices (student_id, term_id, amount) VALUES (1, 1, 100);

-- expect error: a term that ends before it starts
INSERT INTO terms (year, term, starts_on, ends_on) VALUES (2027, 1, '2027-04-01', '2027-01-01');

-- expect error: deleting a guardian whose children are still enrolled
DELETE FROM guardians WHERE id = 7;
