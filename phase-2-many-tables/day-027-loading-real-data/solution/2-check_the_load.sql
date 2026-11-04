-- Check the import: how many counties (counties) and the total population (population).
SELECT COUNT(*) AS counties, SUM(population) AS population FROM counties;
