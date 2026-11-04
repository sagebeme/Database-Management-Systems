-- Create towns: id (numbered automatically, primary key), county_id (required, must be a real county's id), name (VARCHAR(60), required).
CREATE TABLE IF NOT EXISTS towns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    county_id INT NOT NULL,
    name VARCHAR(60) NOT NULL,
    FOREIGN KEY (county_id) REFERENCES counties (id)
);
