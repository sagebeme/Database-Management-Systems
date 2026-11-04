-- For cash and for M-Pesa: the number of sales (sales) and the money (revenue), alphabetical by payment.
SELECT payment, COUNT(*) AS sales, SUM(qty * unit_price) AS revenue
FROM sales
GROUP BY payment
ORDER BY payment;
