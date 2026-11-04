-- Day 97: a boda and taxi app's first four months (made-up data, built by formula so it's the same everywhere).

CREATE TABLE riders (
    id          integer PRIMARY KEY,
    name        text NOT NULL,
    phone       text NOT NULL,
    referred_by integer REFERENCES riders (id),
    banned      boolean NOT NULL DEFAULT false
);

CREATE TABLE drivers (
    id      integer PRIMARY KEY,
    name    text NOT NULL,
    county  text NOT NULL,
    vehicle text NOT NULL CHECK (vehicle IN ('boda', 'tuktuk', 'car'))
);

CREATE TABLE trips (
    id           integer PRIMARY KEY,
    rider_id     integer NOT NULL REFERENCES riders (id),
    driver_id    integer NOT NULL REFERENCES drivers (id),
    requested_at timestamp NOT NULL,
    fare         integer NOT NULL,
    status       text NOT NULL CHECK (status IN ('completed', 'cancelled')),
    payment      text NOT NULL CHECK (payment IN ('mpesa', 'cash')),
    rating       integer CHECK (rating BETWEEN 1 AND 5)
);

INSERT INTO riders (id, name, phone, referred_by, banned)
SELECT i,
       (ARRAY['Wanjiru', 'Otieno', 'Akinyi', 'Kiprop', 'Mwende', 'Baraka', 'Nafula', 'Hassan'])[1 + i % 8] || ' ' ||
       (ARRAY['Kamau', 'Ochieng', 'Mutua', 'Chebet', 'Njoroge', 'Wekesa', 'Ali'])[1 + i % 7],
       '2547' || lpad((10000000 + i * 7331)::text, 8, '0'),
       CASE WHEN i % 3 = 0 THEN i / 3 END,
       i % 13 = 0
FROM generate_series(1, 40) AS i;
-- Two riders signed up twice with the same phone.
UPDATE riders SET phone = (SELECT phone FROM riders WHERE id = 5) WHERE id = 38;
UPDATE riders SET phone = (SELECT phone FROM riders WHERE id = 6) WHERE id = 39;

INSERT INTO drivers (id, name, county, vehicle) VALUES
    (1, 'Juma Mwangi', 'Nairobi', 'boda'), (2, 'Peter Kiprotich', 'Nairobi', 'car'),
    (3, 'Grace Wairimu', 'Nairobi', 'tuktuk'), (4, 'Ali Omar', 'Mombasa', 'tuktuk'),
    (5, 'Halima Said', 'Mombasa', 'boda'), (6, 'Brian Otieno', 'Kisumu', 'boda'),
    (7, 'Esther Adhiambo', 'Kisumu', 'car'), (8, 'Samuel Rotich', 'Nakuru', 'boda'),
    (9, 'Mercy Chepkoech', 'Nakuru', 'car'), (10, 'David Kamau', 'Nairobi', 'boda'),
    (11, 'Faith Njeri', 'Mombasa', 'car'), (12, 'Tom Wafula', 'Kisumu', 'tuktuk');

INSERT INTO trips (id, rider_id, driver_id, requested_at, fare, status, payment, rating)
SELECT i,
       1 + (i * 7) % 34,
       1 + (i * 5 + i / 17) % 12,
       timestamp '2026-01-01 05:00' + ((i * 7919) % 120) * interval '1 day' + ((i * 131) % 1020) * interval '1 minute',
       50 + ((i * 37) % 46) * 10,
       CASE WHEN i % 9 = 0 THEN 'cancelled' ELSE 'completed' END,
       CASE WHEN i % 4 = 0 THEN 'cash' ELSE 'mpesa' END,
       CASE WHEN i % 9 = 0 OR i % 5 = 0 THEN NULL ELSE 1 + (i * i) % 5 END
FROM generate_series(1, 1500) AS i;

-- Some trips were deleted by support.
DELETE FROM trips WHERE id % 97 = 0 OR id BETWEEN 1203 AND 1207;

-- The app double-submitted a few requests.
INSERT INTO trips (id, rider_id, driver_id, requested_at, fare, status, payment, rating)
SELECT 1600 + id, rider_id, driver_id, requested_at, fare, status, payment, NULL
FROM trips WHERE id IN (11, 250, 251, 777, 1450);
INSERT INTO trips (id, rider_id, driver_id, requested_at, fare, status, payment, rating)
SELECT 1700 + id, rider_id, driver_id, requested_at, fare, status, payment, NULL
FROM trips WHERE id = 250;

-- A few riders who kept requesting, minutes apart.
INSERT INTO trips (id, rider_id, driver_id, requested_at, fare, status, payment, rating) VALUES
    (2001, 1, 2, '2026-01-10 08:00', 300, 'cancelled', 'mpesa', NULL),
    (2002, 1, 2, '2026-01-10 08:12', 300, 'cancelled', 'mpesa', NULL),
    (2003, 1, 7, '2026-01-10 08:40', 320, 'completed', 'mpesa', 4),
    (2004, 1, 7, '2026-01-10 09:25', 150, 'completed', 'cash', 5),
    (2005, 2, 4, '2026-01-03 18:00', 100, 'cancelled', 'cash', NULL),
    (2006, 2, 4, '2026-01-03 18:29', 120, 'completed', 'cash', 3),
    (2007, 2, 4, '2026-01-03 18:59', 120, 'completed', 'cash', 3),
    (2008, 34, 9, '2026-02-14 20:00', 500, 'completed', 'mpesa', 5),
    (2009, 34, 3, '2026-02-14 20:15', 90, 'completed', 'mpesa', 5),
    (2010, 34, 6, '2026-02-14 20:31', 60, 'completed', 'mpesa', 2);

-- Not everyone started in January, and not everyone stayed.
UPDATE trips SET rider_id = 33 WHERE rider_id BETWEEN 25 AND 30 AND requested_at < '2026-02-01';
UPDATE trips SET rider_id = 32 WHERE rider_id BETWEEN 25 AND 27 AND requested_at < '2026-03-01';
UPDATE trips SET rider_id = 31 WHERE rider_id BETWEEN 15 AND 20 AND requested_at >= '2026-02-01' AND requested_at < '2026-03-01';
UPDATE trips SET rider_id = 31 WHERE rider_id = 26 AND requested_at >= '2026-04-01';
