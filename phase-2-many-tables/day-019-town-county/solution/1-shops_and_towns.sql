-- Every shop's name (shop), its town (town) and its monthly_sales, biggest first.
SELECT s.name AS shop, t.name AS town, s.monthly_sales
FROM shops AS s
JOIN towns AS t ON s.town_id = t.id
ORDER BY s.monthly_sales DESC;
