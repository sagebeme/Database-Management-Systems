-- Customers who used two or more different agents: phone, name, agents (how many). Most agents first,
-- ties by phone.
-- Write your statement below this line.
SELECT c.phone, c.name, COUNT(DISTINCT t.till) AS agents
FROM customers AS c
JOIN transactions AS t ON t.phone = c.phone
GROUP BY c.phone, c.name
HAVING agents >= 2
ORDER BY agents DESC, c.phone;
