-- id, route and driver of every trip recorded as cashless (details has "cashless": true), by id.
-- Write your statement below this line.
SELECT id, route, details ->> 'driver' AS driver
FROM trips
WHERE details @> '{"cashless": true}'
ORDER BY id;
