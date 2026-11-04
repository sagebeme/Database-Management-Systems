-- Counties with missing rainfall readings: county and missing (how many), most first, ties alphabetical.
SELECT county, COUNT(*) - COUNT(rain_mm) AS missing
FROM readings
GROUP BY county
HAVING COUNT(*) - COUNT(rain_mm) > 0
ORDER BY missing DESC, county;
