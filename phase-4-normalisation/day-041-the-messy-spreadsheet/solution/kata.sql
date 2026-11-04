-- Kata: Fee Rise. In the split design, raise the Physics fee by 10% (to a whole number of shillings), changing exactly one row.
UPDATE subjects SET fee = ROUND(fee * 1.1) WHERE name = 'Physics';
