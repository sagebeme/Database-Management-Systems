-- The names of every shop in Kiambu county, alphabetical.
SELECT name
FROM shops
WHERE town_id IN (
    SELECT id FROM towns WHERE county_id = (SELECT id FROM counties WHERE name = 'Kiambu')
)
ORDER BY name;
