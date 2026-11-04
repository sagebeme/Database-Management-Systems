-- Kata: Empty Counties. Counties with no towns on the list: county, alphabetical.
SELECT c.name AS county
FROM counties AS c
LEFT JOIN towns AS t ON t.county_id = c.id
WHERE t.id IS NULL
ORDER BY county;
