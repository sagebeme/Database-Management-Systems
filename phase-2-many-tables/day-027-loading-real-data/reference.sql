-- The reference table and import, for the tests of the query tasks.
CREATE TABLE IF NOT EXISTS counties (
    code CHAR(3) PRIMARY KEY,
    name VARCHAR(40) NOT NULL UNIQUE,
    former_province VARCHAR(20) NOT NULL,
    capital VARCHAR(40) NOT NULL,
    total_area_km2 INT NOT NULL,
    land_area_km2 INT NOT NULL,
    population INT NOT NULL
);
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
