-- Every town with each of its shops: town and shop (NULL for a town with no shops). Ordered by town, then shop.
SELECT t.name AS town, s.name AS shop
FROM towns AS t
LEFT JOIN shops AS s ON s.town_id = t.id
ORDER BY town, shop;
