-- Create users (id, email, name) if it doesn't exist yet: id counts up by itself, email is required and never
-- repeats, name is optional. Running the file twice must not fail or lose rows.
-- Write your statement below this line.
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
