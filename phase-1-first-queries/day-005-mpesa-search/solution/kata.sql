-- Kata: Brackets Matter. Code and amount of transactions that were Sent or Received AND over 2,000 bob.
SELECT code, amount FROM transactions
WHERE (kind = 'Sent' OR kind = 'Received') AND amount > 2000;
