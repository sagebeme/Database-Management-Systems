-- Names of towns with no shop at all, alphabetical.
SELECT name FROM towns WHERE id NOT IN (SELECT town_id FROM shops) ORDER BY name;
