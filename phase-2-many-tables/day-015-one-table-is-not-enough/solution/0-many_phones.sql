-- Customers who appear with more than one phone number: customer_name and phones (how many different numbers). Alphabetical.
SELECT customer_name, COUNT(DISTINCT customer_phone) AS phones
FROM orders_flat
GROUP BY customer_name
HAVING COUNT(DISTINCT customer_phone) > 1
ORDER BY customer_name;
