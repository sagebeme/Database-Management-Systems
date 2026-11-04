-- Riverwood: a made-up database of Kenyan TV shows (the titles are invented).
-- Shows, genres, which show has which genres, and viewers' ratings out of 10.
--   tools/mysql.sh riverwood < phase-2-many-tables/day-021-shows-and-genres/setup.sql
DROP TABLE IF EXISTS watchlist, tv_show_ratings, tv_show_genres, tv_genres, tv_shows;
CREATE TABLE tv_shows (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(80) NOT NULL,
    first_aired YEAR NOT NULL,
    channel VARCHAR(40) NOT NULL
);
CREATE TABLE tv_genres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(40) NOT NULL UNIQUE
);
INSERT INTO tv_shows (id, title, first_aired, channel) VALUES
    (1, 'Mtaa wa Mapepe', 2016, 'Jamii TV'),
    (2, 'Nairobi Nights', 2019, 'Citi Lights'),
    (3, 'Pwani Love', 2021, 'Bahari TV'),
    (4, 'Kikosi Maalum', 2018, 'Citi Lights'),
    (5, 'Shamba Boys', 2015, 'Jamii TV'),
    (6, 'Mama Pima', 2020, 'Bahari TV'),
    (7, 'Fundi Hacker', 2023, 'Riverwood Plus'),
    (8, 'Matatu Kings', 2017, 'Jamii TV'),
    (9, 'Siri za Lamu', 2022, 'Bahari TV'),
    (10, 'Jiko Wars', 2021, 'Riverwood Plus'),
    (11, 'Kesho Kutwa', 2024, 'Riverwood Plus'),
    (12, 'Shule Yetu', 2014, 'Jamii TV'),
    (13, 'Mwisho wa Reli', 2025, 'Citi Lights');
INSERT INTO tv_genres (id, name) VALUES
    (1, 'Action'),
    (2, 'Comedy'),
    (3, 'Crime'),
    (4, 'Documentary'),
    (5, 'Drama'),
    (6, 'Family'),
    (7, 'Mystery'),
    (8, 'Reality'),
    (9, 'Romance'),
    (10, 'Sci-Fi'),
    (11, 'Thriller');
