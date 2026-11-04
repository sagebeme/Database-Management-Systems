-- Load counties.csv into counties (run from the course folder). The numbers have thousands commas: remove them.
LOAD DATA LOCAL INFILE 'phase-2-many-tables/day-027-loading-real-data/counties.csv'
INTO TABLE counties
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, name, former_province, capital, @total, @land, @population)
SET total_area_km2 = REPLACE(@total, ',', ''),
    land_area_km2 = REPLACE(@land, ',', ''),
    population = REPLACE(@population, ',', '');
