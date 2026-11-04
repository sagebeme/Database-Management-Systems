-- number and stop_count (how many stops) of every route that stops at Westlands, by number.
-- Write your statement below this line.
SELECT number, cardinality(stops) AS stop_count FROM routes WHERE 'Westlands' = ANY (stops) ORDER BY number;
