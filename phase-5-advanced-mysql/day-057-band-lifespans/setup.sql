-- Day 54's artists, and a small library's members and loans (invented). Everything is worked out as of
-- 31 March 2026, so the answers don't change while you work.
--   tools/mysql.sh library < phase-5-advanced-mysql/day-057-band-lifespans/setup.sql
DROP TABLE IF EXISTS artists;
CREATE TABLE artists (
    id INT PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    genre VARCHAR(30) NOT NULL,
    origin VARCHAR(30) NOT NULL,
    fans INT NOT NULL,
    formed YEAR NOT NULL,
    split YEAR NULL
);
INSERT INTO artists VALUES
    (1, 'Ziwa Benga Band', 'Benga', 'Kenya', 420000, 1979, 1998),
    (2, 'Kisima Boys', 'Benga', 'Kenya', 310000, 1985, NULL),
    (3, 'Nyota ya Pwani', 'Taarab', 'Kenya', 180000, 1968, 2004),
    (4, 'Unguja Strings', 'Taarab', 'Tanzania', 260000, 1972, NULL),
    (5, 'Dar Mtaa Crew', 'Bongo Flava', 'Tanzania', 980000, 2004, NULL),
    (6, 'Kariakoo Kings', 'Bongo Flava', 'Tanzania', 760000, 2009, 2019),
    (7, 'Mbagala Stars', 'Bongo Flava', 'Tanzania', 760000, 2011, NULL),
    (8, 'Ndovu Mtaani', 'Gengetone', 'Kenya', 540000, 2017, NULL),
    (9, 'Mathare Vibes', 'Gengetone', 'Kenya', 540000, 2018, 2023),
    (10, 'Buruburu Squad', 'Gengetone', 'Kenya', 220000, 2019, 2022),
    (11, 'Kampala Kadodi', 'Afrobeats', 'Uganda', 610000, 2010, NULL),
    (12, 'Lagos Lagoon Sound', 'Afrobeats', 'Nigeria', 1500000, 2008, NULL),
    (13, 'Ikeja Mainland', 'Afrobeats', 'Nigeria', 890000, 2013, NULL),
    (14, 'Soukous ya Sika', 'Rhumba', 'DR Congo', 1100000, 1975, 2001),
    (15, 'Matonge Express', 'Rhumba', 'DR Congo', 640000, 1988, NULL),
    (16, 'Kigali Hills Choir', 'Gospel', 'Rwanda', 300000, 1995, NULL),
    (17, 'Gulu Praise Team', 'Gospel', 'Uganda', 300000, 2001, NULL),
    (18, 'Kisumu Gospel Voices', 'Gospel', 'Kenya', 450000, 1990, 2015),
    (19, 'Jinja Nile Beat', 'Afrobeats', 'Uganda', 330000, 2012, 2020),
    (20, 'Mombasa Taarab Ensemble', 'Taarab', 'Kenya', 260000, 1959, 1990);
DROP TABLE IF EXISTS loans, members;
CREATE TABLE members (
    id INT PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    born_on DATE NOT NULL
);
INSERT INTO members VALUES
    (1, 'Wanjiku Kamau', '1990-04-12'), (2, 'Otieno Ouma', '1985-03-31'), (3, 'Chebet Rono', '2004-02-29'),
    (4, 'Mutua Musyoka', '1978-12-01'), (5, 'Akinyi Atieno', '2010-04-01'), (6, 'Hassan Ali', '1999-03-30');
CREATE TABLE loans (
    id INT PRIMARY KEY,
    member_id INT NOT NULL,
    book VARCHAR(80) NOT NULL,
    borrowed_on DATE NOT NULL,
    returned_on DATE NULL,
    FOREIGN KEY (member_id) REFERENCES members (id)
);
INSERT INTO loans VALUES
    (1, 1, 'The River Between', '2026-01-05', '2026-01-15'),
    (2, 2, 'Petals of Blood', '2026-01-10', '2026-02-02'),
    (3, 3, 'Coming to Birth', '2026-01-28', '2026-02-11'),
    (4, 4, 'Kidagaa Kimemwozea', '2026-01-02', NULL),
    (5, 5, 'Blossoms of the Savannah', '2026-02-14', '2026-02-27'),
    (6, 1, 'Weep Not, Child', '2026-02-20', NULL),
    (7, 6, 'Dust', '2026-03-02', '2026-03-14'),
    (8, 2, 'Going Down River Road', '2026-03-10', NULL),
    (9, 3, 'The Upright Revolution', '2026-03-20', NULL),
    (10, 4, 'Siku Njema', '2026-03-28', NULL);
