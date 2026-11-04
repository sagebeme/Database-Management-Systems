-- Kata: Same Name. Towns that have the same name as their county: town, alphabetical.
SELECT t.name AS town
FROM towns AS t
JOIN counties AS c ON t.county_id = c.id
WHERE t.name = c.name
ORDER BY town;
