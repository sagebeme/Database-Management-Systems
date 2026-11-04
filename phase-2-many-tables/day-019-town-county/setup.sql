-- Counties and towns from Day 17 (real), plus shops on a delivery app's books (made up).
--   tools/mysql.sh places < phase-2-many-tables/day-019-town-county/setup.sql
DROP TABLE IF EXISTS shops, wards, towns, counties;
CREATE TABLE counties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code CHAR(3) NOT NULL UNIQUE,
    name VARCHAR(60) NOT NULL UNIQUE
);
CREATE TABLE towns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    county_id INT NOT NULL,
    name VARCHAR(60) NOT NULL,
    FOREIGN KEY (county_id) REFERENCES counties (id)
);
CREATE TABLE shops (
    id INT AUTO_INCREMENT PRIMARY KEY,
    town_id INT NOT NULL,
    name VARCHAR(60) NOT NULL,
    monthly_sales INT NOT NULL,
    FOREIGN KEY (town_id) REFERENCES towns (id)
);
INSERT INTO counties (id, code, name) VALUES
    (1, '001', 'Mombasa'),
    (2, '016', 'Machakos'),
    (3, '022', 'Kiambu'),
    (4, '027', 'Uasin Gishu'),
    (5, '032', 'Nakuru'),
    (6, '042', 'Kisumu'),
    (7, '047', 'Nairobi');
INSERT INTO towns (id, county_id, name) VALUES
    (1, 1, 'Mombasa'),
    (2, 2, 'Machakos'),
    (3, 2, 'Athi River'),
    (4, 3, 'Thika'),
    (5, 3, 'Ruiru'),
    (6, 3, 'Kikuyu'),
    (7, 3, 'Limuru'),
    (8, 4, 'Eldoret'),
    (9, 5, 'Nakuru'),
    (10, 5, 'Naivasha'),
    (11, 5, 'Molo'),
    (12, 6, 'Kisumu'),
    (13, 6, 'Maseno'),
    (14, 5, 'Gilgil'),
    (15, 7, 'Nairobi');
INSERT INTO shops (id, town_id, name, monthly_sales) VALUES
    (1, 9, 'Mama Mboga Fresh', 132000),
    (2, 10, 'Kilimo Agrovet', 102000),
    (3, 10, 'Lakeside Hardware', 378000),
    (4, 10, 'Naivasha Pharmacy', 269000),
    (5, 11, 'Molo Dairy Point', 211000),
    (6, 4, 'Thika Road Spares', 162000),
    (7, 5, 'Ruiru Boutique', 141000),
    (8, 7, 'Limuru Tea Room', 290000),
    (9, 8, 'Eldoret Grains', 361000),
    (10, 9, 'Rift Valley Butchery', 292000),
    (11, 12, 'Kisumu Fish Market', 133000),
    (12, 12, 'Nyanza Electronics', 285000),
    (13, 1, 'Mombasa Spice House', 191000),
    (14, 1, 'Old Town Tailors', 274000),
    (15, 2, 'Machakos Fruit Stall', 175000),
    (16, 15, 'CBD Phone Repairs', 140000),
    (17, 15, 'Westgate Books', 169000),
    (18, 14, 'Gilgil Mechanics', 394000);
