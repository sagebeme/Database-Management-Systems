-- Create riders: id (auto-numbered primary key), name (VARCHAR(60), required), licence_no (CHAR(9), required, unique)
-- and age (TINYINT, required, from 18 to 70).
CREATE TABLE IF NOT EXISTS riders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    licence_no CHAR(9) NOT NULL UNIQUE,
    age TINYINT NOT NULL CHECK (age BETWEEN 18 AND 70)
);
