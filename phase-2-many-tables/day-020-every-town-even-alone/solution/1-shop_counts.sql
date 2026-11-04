-- Every town and how many shops it has (shops), including towns with none. Most first, ties alphabetical.
SELECT t.name AS town, COUNT(s.id) AS shops
FROM towns AS t
LEFT JOIN shops AS s ON s.town_id = t.id
GROUP BY t.id, t.name
ORDER BY shops DESC, town;
