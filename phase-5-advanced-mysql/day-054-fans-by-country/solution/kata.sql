-- The origin (or origins, if tied) with the second-highest total fans: origin, nb_fans.
-- Write your statement below this line.
SELECT origin, nb_fans
FROM (
    SELECT origin, SUM(fans) AS nb_fans, DENSE_RANK() OVER (ORDER BY SUM(fans) DESC) AS r
    FROM artists
    GROUP BY origin
) AS ranked
WHERE r = 2
ORDER BY origin;
