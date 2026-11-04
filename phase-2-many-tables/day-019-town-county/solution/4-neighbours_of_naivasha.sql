-- The other towns in the same county as Naivasha (not Naivasha itself): name, alphabetical.
SELECT other.name
FROM towns AS naivasha
JOIN towns AS other ON other.county_id = naivasha.county_id
WHERE naivasha.name = 'Naivasha' AND other.id <> naivasha.id
ORDER BY other.name;
