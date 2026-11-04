-- Code, counterparty and amount of every Sent transaction over 1,000 bob.
SELECT code, counterparty, amount FROM transactions WHERE kind = 'Sent' AND amount > 1000;
