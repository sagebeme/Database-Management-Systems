-- Each county's name (county) and its shops' total monthly sales (sales), biggest first.
SELECT c.name AS county, SUM(s.monthly_sales) AS sales
FROM shops AS s
JOIN towns AS t ON s.town_id = t.id
JOIN counties AS c ON t.county_id = c.id
GROUP BY c.id, c.name
ORDER BY sales DESC;
