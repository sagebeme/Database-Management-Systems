-- Code, counterparty and amount of every payment to KPLC (prepaid or postpaid).
SELECT code, counterparty, amount FROM transactions WHERE counterparty LIKE 'KPLC%';
