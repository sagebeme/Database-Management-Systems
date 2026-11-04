-- The id and name of every town in Nakuru county, in id order. Look Nakuru up by name.
SELECT id, name
FROM towns
WHERE county_id = (SELECT id FROM counties WHERE name = 'Nakuru')
ORDER BY id;
