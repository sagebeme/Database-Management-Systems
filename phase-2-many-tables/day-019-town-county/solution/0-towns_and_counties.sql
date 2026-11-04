-- Every town's id, its name (town) and its county's name (county), in town id order.
SELECT towns.id, towns.name AS town, counties.name AS county
FROM towns
JOIN counties ON towns.county_id = counties.id
ORDER BY towns.id;
