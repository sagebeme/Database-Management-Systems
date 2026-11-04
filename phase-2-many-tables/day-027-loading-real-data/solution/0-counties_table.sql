-- Create counties: code CHAR(3) primary key; name (VARCHAR(40), required, unique); former_province (VARCHAR(20)), capital (VARCHAR(40)), total_area_km2, land_area_km2 and population (INT), all required.
CREATE TABLE IF NOT EXISTS counties (
    code CHAR(3) PRIMARY KEY,
    name VARCHAR(40) NOT NULL UNIQUE,
    former_province VARCHAR(20) NOT NULL,
    capital VARCHAR(40) NOT NULL,
    total_area_km2 INT NOT NULL,
    land_area_km2 INT NOT NULL,
    population INT NOT NULL
);
