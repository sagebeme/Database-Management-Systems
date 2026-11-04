-- Create counties: id (numbered automatically, primary key), code (CHAR(3), required, unique), name (VARCHAR(60), required, unique).
CREATE TABLE IF NOT EXISTS counties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code CHAR(3) NOT NULL UNIQUE,
    name VARCHAR(60) NOT NULL UNIQUE
);
