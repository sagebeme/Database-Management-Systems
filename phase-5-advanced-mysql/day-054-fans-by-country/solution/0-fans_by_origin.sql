-- Each origin and its total fans (nb_fans), most first.
-- Write your statement below this line.
SELECT origin, SUM(fans) AS nb_fans
FROM artists
GROUP BY origin
ORDER BY nb_fans DESC;
