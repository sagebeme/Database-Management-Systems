-- Kata: Unknowns Last. Name and credit_limit of every customer, biggest limit first, customers with an unknown limit at the end (alphabetical among themselves).
SELECT name, credit_limit FROM customers
ORDER BY credit_limit IS NULL, credit_limit DESC, name;
