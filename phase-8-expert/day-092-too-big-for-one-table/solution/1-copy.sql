-- Copy every row of payments_old into payments.
INSERT INTO payments SELECT id, paid_on, phone, amount FROM payments_old;
