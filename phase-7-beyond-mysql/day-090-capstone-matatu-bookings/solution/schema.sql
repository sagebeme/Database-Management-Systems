-- The bookings database, in PostgreSQL:
--   routes:   number (TEXT, the primary key), fare (INT, required, above 0)
--   trips:    id (an identity column, the primary key), route (TEXT, required, a route), departs (TIMESTAMPTZ,
--             required), seats (INT, required, 1 to 70)
--   bookings: id (identity, primary key), trip_id (INT, required, a trip), seat (INT, required, 1 or more),
--             phone (TEXT, required), booked_at (TIMESTAMPTZ, required, now by default);
--             a seat can be booked only once per trip.

CREATE TABLE routes (
    number TEXT PRIMARY KEY,
    fare INT NOT NULL CHECK (fare > 0)
);
CREATE TABLE trips (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    route TEXT NOT NULL REFERENCES routes (number),
    departs TIMESTAMPTZ NOT NULL,
    seats INT NOT NULL CHECK (seats BETWEEN 1 AND 70)
);
CREATE TABLE bookings (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    trip_id INT NOT NULL REFERENCES trips (id),
    seat INT NOT NULL CHECK (seat >= 1),
    phone TEXT NOT NULL,
    booked_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (trip_id, seat)
);
