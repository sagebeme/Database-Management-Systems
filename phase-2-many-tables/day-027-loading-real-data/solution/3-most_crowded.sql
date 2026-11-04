-- The 5 most crowded counties, by people per km2 of land: county, density (a whole number). Most crowded first.
SELECT name AS county, ROUND(population / land_area_km2) AS density
FROM counties
ORDER BY population / land_area_km2 DESC
LIMIT 5;
