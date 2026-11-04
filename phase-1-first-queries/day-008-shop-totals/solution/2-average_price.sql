-- The average unit price of a sale, rounded to 2 places, in a column called average_price.
SELECT ROUND(AVG(unit_price), 2) AS average_price FROM sales;
