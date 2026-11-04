# Day 21: Riverwood: Shows and Genres

## The brief

Riverwood Plus is a new streaming app for Kenyan shows, and its catalogue team, led by Brenda, is setting up the database. A show can have several genres (*Siri za Lamu* is a drama, a mystery and a romance), and a genre has many shows. That's a **many-to-many** relationship, and no single foreign key can hold it: a show can't have a `genre_id` column (which one?), and a genre can't have a `show_id`.

The answer is a third table in between, with one row per show–genre pair. It's called a **junction table** (or link, or bridge table).

```
tv_shows               tv_show_genres            tv_genres
+----+--------------+  +---------+----------+    +----+---------+
| id | title        |  | show_id | genre_id |    | id | name    |
+----+--------------+  +---------+----------+    +----+---------+
|  9 | Siri za Lamu | -|       9 |        5 |--> |  5 | Drama   |
|    |              | -|       9 |        7 |--> |  7 | Mystery |
|    |              | -|       9 |        9 |--> |  9 | Romance |
+----+--------------+  +---------+----------+    +----+---------+
```

`setup.sql` creates `tv_shows` (13 invented shows) and `tv_genres` (11 genres). You make the junction table; then `links.sql` fills it.

## What you'll use

A junction table is two foreign keys whose **pair** is the primary key:

```sql
CREATE TABLE IF NOT EXISTS enrolments (
    student_id INT NOT NULL,
    unit_id INT NOT NULL,
    PRIMARY KEY (student_id, unit_id),
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (unit_id) REFERENCES units (id)
);
```

To go from a show to its genres, you join *through* the junction: shows → links → genres. That's two joins for one relationship.

```sql
SELECT s.title, g.name
FROM tv_shows AS s
JOIN tv_show_genres AS sg ON sg.show_id = s.id
JOIN tv_genres AS g ON g.id = sg.genre_id;
```

- Shows with no genres, or genres with no shows, need `LEFT JOIN` all the way through. If the second join is a plain `JOIN`, it throws away the rows the first `LEFT JOIN` kept.
- "Both Drama **and** Romance" can't be `WHERE g.name = 'Drama' AND g.name = 'Romance'`: one row has one genre. Keep rows that are either, group by show, and keep shows that matched both: `HAVING COUNT(DISTINCT g.name) = 2`.
- A junction table can carry facts about the pair itself: a `role` in `actors_in_shows`, a `grade` in `enrolments`.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS riverwood;"
tools/mysql.sh riverwood < phase-2-many-tables/day-021-shows-and-genres/setup.sql
```

1. `starter/0-junction_table.sql`: create `tv_show_genres`: `show_id` and `genre_id`, both required, both pointing at real rows, each pair at most once. Then load the links: `tools/mysql.sh riverwood < phase-2-many-tables/day-021-shows-and-genres/links.sql`
2. `starter/1-genres_of_nairobi_nights.sql`: genres of *Nairobi Nights*: `name`, alphabetical.
3. `starter/2-comedies.sql`: titles of every comedy, alphabetical.
4. `starter/3-shows_per_genre.sql`: `genre` and `number_of_shows`, for genres with at least one show. Most first, ties alphabetical.
5. `starter/4-every_show_and_genre.sql`: every show with each genre: `title`, `genre` (`NULL` for a show with none). Ordered by title, then genre.
6. `pytest phase-2-many-tables/day-021-shows-and-genres`

## The kata: Romance and Drama

In `starter/kata.sql`, list titles of shows that are both Drama and Romance, alphabetical.

## When you're stuck

- **`links.sql` fails with `Unknown column`**: your columns must be called `show_id` and `genre_id`.
- **`ERROR 1068: Multiple primary key defined`**: one `PRIMARY KEY (show_id, genre_id)`, not one on each column.
- **Mwisho wa Reli is missing from step 5**: both joins must be `LEFT JOIN`.
- **The kata returns nothing**: a single row can't be two genres at once. Group and count.
