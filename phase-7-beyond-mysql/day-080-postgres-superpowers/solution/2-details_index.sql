-- A GIN index called idx_trips_details on trips.details, so that containment searches like the one in
-- 0-cashless_trips.sql can use it.
-- Write your statement below this line.
CREATE INDEX idx_trips_details ON trips USING GIN (details);
