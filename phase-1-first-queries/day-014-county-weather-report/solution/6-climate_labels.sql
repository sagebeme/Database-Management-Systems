-- Each county, its avg_max (1 place) and a label: hot (average high 30 or more), warm (24 or more) or cool. Alphabetical.
SELECT county,
       ROUND(AVG(max_c), 1) AS avg_max,
       CASE
           WHEN AVG(max_c) >= 30 THEN 'hot'
           WHEN AVG(max_c) >= 24 THEN 'warm'
           ELSE 'cool'
       END AS label
FROM readings
GROUP BY county
ORDER BY county;
