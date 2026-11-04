-- Add the town Gilgil to Nakuru county without typing Nakuru's id: look it up by name in the same statement.
INSERT INTO towns (county_id, name)
SELECT id, 'Gilgil' FROM counties WHERE name = 'Nakuru';
