-- Kata: one row per route, by number: number, and trips, a JSON array (jsonb) of that route's trips as objects
-- {"id": ..., "driver": ...}, by trip id. A route with no trips gets [].
-- Write your statement below this line.
SELECT r.number,
       COALESCE(jsonb_agg(jsonb_build_object('id', t.id, 'driver', t.details ->> 'driver') ORDER BY t.id)
                FILTER (WHERE t.id IS NOT NULL), '[]'::jsonb) AS trips
FROM routes AS r
LEFT JOIN trips AS t ON t.route = r.number
GROUP BY r.number
ORDER BY r.number;
