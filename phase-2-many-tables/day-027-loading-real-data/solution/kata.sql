-- Kata: Counties on the Water. Counties where water is at least 10% of the total area: county, water_percent (1 decimal place). Most water first.
SELECT name AS county,
       ROUND((total_area_km2 - land_area_km2) * 100 / total_area_km2, 1) AS water_percent
FROM counties
WHERE (total_area_km2 - land_area_km2) * 100 / total_area_km2 >= 10
ORDER BY (total_area_km2 - land_area_km2) / total_area_km2 DESC;
