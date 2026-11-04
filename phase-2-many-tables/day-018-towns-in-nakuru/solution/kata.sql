-- Kata: The Average Town. Add up each town's shop sales, then average those totals over the towns that have shops: avg_town_sales, rounded to a whole number.
SELECT ROUND(AVG(total)) AS avg_town_sales
FROM (SELECT town_id, SUM(monthly_sales) AS total FROM shops GROUP BY town_id) AS town_totals;
