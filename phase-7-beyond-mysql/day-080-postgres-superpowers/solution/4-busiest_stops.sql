-- Every stop, with routes: how many routes stop there. Most first; ties alphabetical.
-- Write your statement below this line.
SELECT stop, count(*) AS routes
FROM routes, unnest(stops) AS stop
GROUP BY stop
ORDER BY routes DESC, stop;
