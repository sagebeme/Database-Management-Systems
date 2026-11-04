-- Towns with no shops, found with a join this time: town, alphabetical.
SELECT t.name AS town
FROM towns AS t
LEFT JOIN shops AS s ON s.town_id = t.id
WHERE s.id IS NULL
ORDER BY town;
