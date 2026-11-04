-- question: What came in on one day? (The bursar reconciles against the M-Pesa statement.)
SELECT p.mpesa_receipt, p.amount, p.paid_at
FROM payments p
WHERE p.paid_at >= '2026-02-14' AND p.paid_at < '2026-02-15'
ORDER BY p.paid_at;
