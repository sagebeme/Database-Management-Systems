-- The flat ledger again, from the new tables, clean: code, done_at, till, agent_name, location, phone,
-- customer_name, type, amount, commission. Oldest first, ties by code.
-- Write your statement below this line.
SELECT t.code, t.done_at, a.till, a.name AS agent_name, a.location, c.phone, c.name AS customer_name,
       t.type, t.amount, t.commission
FROM transactions AS t
JOIN agents AS a ON a.till = t.till
JOIN customers AS c ON c.phone = t.phone
ORDER BY t.done_at, t.code;
