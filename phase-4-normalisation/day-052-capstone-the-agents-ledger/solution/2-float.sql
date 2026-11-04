-- For every agent: till, name, deposits (total amount), withdrawals (total amount), commission (total).
-- 0, not NULL, when there's nothing. In till order.
-- Write your statement below this line.
SELECT a.till, a.name,
       COALESCE(SUM(CASE WHEN t.type = 'Deposit' THEN t.amount END), 0) AS deposits,
       COALESCE(SUM(CASE WHEN t.type = 'Withdrawal' THEN t.amount END), 0) AS withdrawals,
       COALESCE(SUM(t.commission), 0) AS commission
FROM agents AS a
LEFT JOIN transactions AS t ON t.till = a.till
GROUP BY a.till, a.name
ORDER BY a.till;
