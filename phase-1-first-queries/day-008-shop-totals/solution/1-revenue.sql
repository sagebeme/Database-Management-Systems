-- Total money taken (quantity times unit price, added up), in a column called revenue.
SELECT SUM(qty * unit_price) AS revenue FROM sales;
