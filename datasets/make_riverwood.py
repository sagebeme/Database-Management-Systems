"""Writes the Riverwood TV database used on Days 21-23, 26 and 28: python datasets/make_riverwood.py

Riverwood is what Kenya's film industry calls itself. The shows below are invented; any
resemblance to real titles is a coincidence.
"""
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SHOWS = [  # id, title, first aired, channel, genres
    (1, "Mtaa wa Mapepe", 2016, "Jamii TV", ["Comedy"]),
    (2, "Nairobi Nights", 2019, "Citi Lights", ["Crime", "Drama"]),
    (3, "Pwani Love", 2021, "Bahari TV", ["Drama", "Romance"]),
    (4, "Kikosi Maalum", 2018, "Citi Lights", ["Action", "Crime"]),
    (5, "Shamba Boys", 2015, "Jamii TV", ["Comedy", "Family"]),
    (6, "Mama Pima", 2020, "Bahari TV", ["Drama"]),
    (7, "Fundi Hacker", 2023, "Riverwood Plus", ["Crime", "Thriller"]),
    (8, "Matatu Kings", 2017, "Jamii TV", ["Action", "Comedy"]),
    (9, "Siri za Lamu", 2022, "Bahari TV", ["Drama", "Mystery", "Romance"]),
    (10, "Jiko Wars", 2021, "Riverwood Plus", ["Reality"]),
    (11, "Kesho Kutwa", 2024, "Riverwood Plus", ["Sci-Fi", "Thriller"]),
    (12, "Shule Yetu", 2014, "Jamii TV", ["Comedy", "Family"]),
    (13, "Mwisho wa Reli", 2025, "Citi Lights", []),
]
GENRES = ["Action", "Comedy", "Crime", "Documentary", "Drama", "Family", "Mystery", "Reality", "Romance", "Sci-Fi", "Thriller"]


def q(s):
    return "'" + s.replace("'", "''") + "'"


def base(with_links=True, with_ratings=True, with_watchlist=False):
    out = [
        "DROP TABLE IF EXISTS watchlist, tv_show_ratings, tv_show_genres, tv_genres, tv_shows;",
        "CREATE TABLE tv_shows (\n    id INT AUTO_INCREMENT PRIMARY KEY,\n    title VARCHAR(80) NOT NULL,\n"
        "    first_aired YEAR NOT NULL,\n    channel VARCHAR(40) NOT NULL\n);",
        "CREATE TABLE tv_genres (\n    id INT AUTO_INCREMENT PRIMARY KEY,\n    name VARCHAR(40) NOT NULL UNIQUE\n);",
    ]
    out.append("INSERT INTO tv_shows (id, title, first_aired, channel) VALUES\n" + ",\n".join(
        f"    ({i}, {q(t)}, {y}, {q(c)})" for i, t, y, c, _ in SHOWS) + ";")
    out.append("INSERT INTO tv_genres (id, name) VALUES\n" + ",\n".join(
        f"    ({i}, {q(g)})" for i, g in enumerate(GENRES, 1)) + ";")
    if with_links:
        out.append(JUNCTION_DDL)
        out.append(links())
    if with_ratings:
        out.append("CREATE TABLE tv_show_ratings (\n    show_id INT NOT NULL,\n    rate TINYINT NOT NULL,\n"
                   "    FOREIGN KEY (show_id) REFERENCES tv_shows (id)\n);")
        out.append(ratings())
    if with_watchlist:
        out.append(WATCHLIST)
    return "\n".join(out) + "\n"


JUNCTION_DDL = ("CREATE TABLE tv_show_genres (\n    show_id INT NOT NULL,\n    genre_id INT NOT NULL,\n"
                "    PRIMARY KEY (show_id, genre_id),\n    FOREIGN KEY (show_id) REFERENCES tv_shows (id),\n"
                "    FOREIGN KEY (genre_id) REFERENCES tv_genres (id)\n);")


def links():
    pairs = [(i, GENRES.index(g) + 1) for i, _, _, _, gs in SHOWS for g in gs]
    return "INSERT INTO tv_show_genres (show_id, genre_id) VALUES\n" + ",\n".join(
        f"    ({s}, {g})" for s, g in pairs) + ";"


def ratings():
    random.seed(23)
    rows = []
    for i, *_ in SHOWS:
        if i == 13:
            continue  # too new to have ratings
        mean = random.uniform(5, 9)
        for _ in range(random.randint(3, 7)):
            rows.append((i, max(1, min(10, round(random.gauss(mean, 1.5))))))
    return "INSERT INTO tv_show_ratings (show_id, rate) VALUES\n" + ",\n".join(
        f"    ({s}, {r})" for s, r in rows) + ";"


# Viewers' saved shows. show_id is NULL when a viewer saved a title Riverwood doesn't have yet:
# exactly the row that makes `NOT IN (SELECT show_id FROM watchlist)` return nothing (Day 22).
WATCHLIST = """CREATE TABLE watchlist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    viewer VARCHAR(40) NOT NULL,
    show_id INT NULL,
    requested_title VARCHAR(80) NULL,
    FOREIGN KEY (show_id) REFERENCES tv_shows (id)
);
INSERT INTO watchlist (viewer, show_id, requested_title) VALUES
    ('akinyi', 2, NULL),
    ('akinyi', 9, NULL),
    ('baraka', 4, NULL),
    ('baraka', 2, NULL),
    ('chebet', 5, NULL),
    ('chebet', 12, NULL),
    ('chebet', NULL, 'Boda Boda Diaries'),
    ('dennis', 7, NULL),
    ('dennis', 11, NULL);"""


HEADER = """-- Riverwood: a made-up database of Kenyan TV shows (the titles are invented).
-- Shows, genres, which show has which genres, and viewers' ratings out of 10.
--   tools/mysql.sh riverwood < {path}
"""

if __name__ == "__main__":
    for day, kwargs in [
        ("phase-2-many-tables/day-021-shows-and-genres", dict(with_links=False, with_ratings=False)),
        ("phase-2-many-tables/day-022-not-a-comedy", dict(with_watchlist=True)),
        ("phase-2-many-tables/day-023-ratings", {}),
        ("phase-2-many-tables/day-026-views", dict(with_watchlist=True)),
        ("phase-2-many-tables/day-028-capstone-the-riverwood-report", dict(with_watchlist=True)),
    ]:
        folder = ROOT / day
        (folder / "starter").mkdir(parents=True, exist_ok=True)
        (folder / "solution").mkdir(parents=True, exist_ok=True)
        (folder / "setup.sql").write_text(HEADER.format(path=f"{day}/setup.sql") + base(**kwargs))
    (ROOT / "phase-2-many-tables/day-021-shows-and-genres/links.sql").write_text(
        "-- Which show has which genres. Run it after your 0-junction_table.sql:\n"
        "--   tools/mysql.sh riverwood < phase-2-many-tables/day-021-shows-and-genres/links.sql\n" + links() + "\n")
