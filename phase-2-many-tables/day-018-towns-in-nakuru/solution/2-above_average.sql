-- Name and monthly_sales of shops that sell more than the average shop, biggest first.
SELECT name, monthly_sales
FROM shops
WHERE monthly_sales > (SELECT AVG(monthly_sales) FROM shops)
ORDER BY monthly_sales DESC;
