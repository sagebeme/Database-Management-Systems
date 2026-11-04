-- Every town and every driver: town and driver, NULL where there's no match on the other side. Towns alphabetical, drivers with no town last; drivers alphabetical within.
SELECT t.name AS town, d.name AS driver
FROM towns AS t
LEFT JOIN drivers AS d ON d.town_id = t.id
UNION
SELECT t.name AS town, d.name AS driver
FROM towns AS t
RIGHT JOIN drivers AS d ON d.town_id = t.id
ORDER BY town IS NULL, town, driver;
