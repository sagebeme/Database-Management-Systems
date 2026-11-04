-- Twenty East and Central African acts on a streaming app (invented names and numbers).
--   tools/mysql.sh music < phase-5-advanced-mysql/day-054-fans-by-country/setup.sql
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
