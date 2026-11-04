-- Route 44 to Githurai, run by Kilele Movers, fare 90. If route 44 is already there, set its destination,
-- sacco and fare to these instead. One statement; look the sacco up by name.
-- Write your statement below this line.
INSERT INTO routes (number, destination, sacco_id, fare)
SELECT '44', 'Githurai', id, 90 FROM saccos WHERE name = 'Kilele Movers'
ON CONFLICT (number) DO UPDATE
SET destination = EXCLUDED.destination, sacco_id = EXCLUDED.sacco_id, fare = EXCLUDED.fare;
