-- Take January out of payments, keeping its rows in payments_2026_01 as an ordinary table of its own.
ALTER TABLE payments DETACH PARTITION payments_2026_01;
