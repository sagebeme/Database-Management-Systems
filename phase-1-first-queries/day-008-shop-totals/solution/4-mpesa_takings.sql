-- How many sales were paid by M-Pesa and how much they came to, in columns mpesa_sales and mpesa_revenue.
SELECT COUNT(*) AS mpesa_sales, SUM(qty * unit_price) AS mpesa_revenue
FROM sales
WHERE payment = 'mpesa';
