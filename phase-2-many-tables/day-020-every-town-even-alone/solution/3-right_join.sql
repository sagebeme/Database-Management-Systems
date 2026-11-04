-- The same answer as 1-shop_counts, written with RIGHT JOIN (shops on the left).
SELECT t.name AS town, COUNT(s.id) AS shops
FROM shops AS s
RIGHT JOIN towns AS t ON s.town_id = t.id
GROUP BY t.id, t.name
ORDER BY shops DESC, town;
