-- id, passengers (how many fares in the trip's "fares" array) and takings (their sum) for every trip, by id.
-- A trip with no fares has 0 passengers and 0 takings.
-- Write your statement below this line.
SELECT t.id,
       jsonb_array_length(t.details -> 'fares') AS passengers,
       COALESCE((SELECT SUM(f::int) FROM jsonb_array_elements_text(t.details -> 'fares') AS f), 0) AS takings
FROM trips AS t
ORDER BY t.id;
