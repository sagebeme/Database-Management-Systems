-- Every shop with its town and county: shop, town, county. Ordered by county, then shop.
SELECT s.name AS shop, t.name AS town, c.name AS county
FROM shops AS s
JOIN towns AS t ON s.town_id = t.id
JOIN counties AS c ON t.county_id = c.id
ORDER BY county, shop;
