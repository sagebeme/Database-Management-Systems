-- Add seats to vehicles: INT, required, 14 for every vehicle already there and by default, and between 1 and 70.
ALTER TABLE vehicles ADD COLUMN seats INT NOT NULL DEFAULT 14 CHECK (seats BETWEEN 1 AND 70);
