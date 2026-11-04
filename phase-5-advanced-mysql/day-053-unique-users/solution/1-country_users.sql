-- The same users table (if it doesn't exist yet), plus country: one of KE, UG, TZ, RW, BI, SS, required,
-- 'KE' when it isn't given.
-- Write your statement below this line.
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    country ENUM('KE', 'UG', 'TZ', 'RW', 'BI', 'SS') NOT NULL DEFAULT 'KE'
);
