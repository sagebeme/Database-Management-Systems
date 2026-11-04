-- Create wards: id (auto, primary key), town_id (required, a real town), name (VARCHAR(60), required). Deleting a town deletes its wards.
CREATE TABLE IF NOT EXISTS wards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    town_id INT NOT NULL,
    name VARCHAR(60) NOT NULL,
    FOREIGN KEY (town_id) REFERENCES towns (id) ON DELETE CASCADE
);
