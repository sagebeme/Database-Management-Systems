-- Create constituencies: id (auto-numbered primary key), name (VARCHAR(60), required) and county_code,
-- so that every constituency is in exactly one real county.
CREATE TABLE IF NOT EXISTS constituencies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    county_code CHAR(3) NOT NULL,
    FOREIGN KEY (county_code) REFERENCES counties (code)
);
