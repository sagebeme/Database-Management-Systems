-- Create trips: id (auto-numbered primary key), plate (required, a real bike), fare (INT, required, more than 0),
-- started_at (DATETIME, required), ended_at (DATETIME, optional, after started_at if given).
-- Deleting a bike deletes its trips; changing a bike's plate changes its trips' plate.
CREATE TABLE IF NOT EXISTS trips (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plate VARCHAR(10) NOT NULL,
    fare INT NOT NULL CHECK (fare > 0),
    started_at DATETIME NOT NULL,
    ended_at DATETIME NULL,
    CHECK (ended_at IS NULL OR ended_at > started_at),
    FOREIGN KEY (plate) REFERENCES bikes (plate) ON DELETE CASCADE ON UPDATE CASCADE
);
