-- Create bikes: plate (VARCHAR(10), primary key), rider_id (optional, a real rider), engine_cc (SMALLINT, required, 50 to 1000).
-- If a rider is deleted, their bikes stay with no rider. If a rider's id changes, their bikes follow.
CREATE TABLE IF NOT EXISTS bikes (
    plate VARCHAR(10) PRIMARY KEY,
    rider_id INT NULL,
    engine_cc SMALLINT NOT NULL CHECK (engine_cc BETWEEN 50 AND 1000),
    FOREIGN KEY (rider_id) REFERENCES riders (id) ON DELETE SET NULL ON UPDATE CASCADE
);
