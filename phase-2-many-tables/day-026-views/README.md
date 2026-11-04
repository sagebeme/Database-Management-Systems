# Day 26: Views

## The brief

Brenda's analysts keep pasting the same three-table join at the top of every report, and each copy is slightly different. One counts Mwisho wa Reli and one forgets it; one rounds averages and one doesn't. The website team has a different worry: their admin page for Jamii TV's desk should only ever touch Jamii TV's shows.

A **view** is a saved `SELECT` with a name. You query it like a table, but it holds no rows of its own: every time you read it, MySQL runs the query underneath against the live tables. Write the join once, name it, and everyone uses the same one.

`setup.sql` loads the full Riverwood database: shows, genres, ratings and the watchlist.

## What you'll use

```sql
CREATE VIEW show_titles AS
SELECT id, title FROM tv_shows;

SELECT * FROM show_titles WHERE title LIKE 'S%';   -- a view is used like a table

CREATE OR REPLACE VIEW show_titles AS ...;          -- change it (or create it if missing)
DROP VIEW IF EXISTS show_titles;
SHOW FULL TABLES;                                   -- Table_type says BASE TABLE or VIEW
```

- **A view is always up to date**, because it's a query, not a copy. `CREATE TABLE ... AS SELECT` (Day 15) is a copy that goes stale the moment the data changes.
- **Views can use views.** Build small ones (`show_scores`) and combine them.
- **Name every computed column** in a view: `ROUND(AVG(r.rate), 2) AS average`. The column names are what people query.
- **`GROUP_CONCAT`** joins a group's values into one string, a handy column for a view:

  ```sql
  GROUP_CONCAT(g.name ORDER BY g.name SEPARATOR ', ')   -- 'Drama, Mystery, Romance'
  ```

  If every value in the group is `NULL`, the result is `NULL`.

- **Some views accept writes.** If a view reads one table, with no `GROUP BY`, `DISTINCT` or aggregates, you can `INSERT` and `UPDATE` through it, and the rows land in the table. **`WITH CHECK OPTION`** refuses any write that would produce a row the view itself can't see, such as a Jamii TV desk moving a show to another channel.
- **Views and privileges go together**: `GRANT SELECT ON riverwood.catalogue TO ...` gives an account the view's columns and rows without access to the tables behind it.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS riverwood;"
tools/mysql.sh riverwood < phase-2-many-tables/day-026-views/setup.sql
```

The tests change the tables after creating your view, and check the view kept up.

1. `starter/0-catalogue_view.sql`: create the view `catalogue`: `title`, `channel`, `first_aired`, and `genres` (the show's genre names, alphabetical, joined by `', '`; `NULL` for no genre). Every show.
2. `starter/1-show_scores_view.sql`: create the view `show_scores`: `show_id`, `title`, `votes` (0 if none) and `average` (2 places; `NULL` if no votes). Every show.
3. `starter/2-top_three.sql`: using `show_scores`, the 3 best shows by `average` among those with at least 5 votes: `title`, `average`. Ties alphabetical.
4. `starter/3-catalogue_with_scores.sql`: replace `catalogue` so it also has `average` (from `show_scores`) as its last column. The file must work twice.
5. `starter/4-jamii_desk.sql`: create the view `jamii_shows` (`id`, `title`, `first_aired`, `channel`) of Jamii TV's shows, refusing writes that would leave Jamii TV.
6. `pytest phase-2-many-tables/day-026-views`

## The kata: The Genre Board

In `starter/kata.sql`, create the view `genre_board`: `genre`, `shows`, `votes` and `average` (2 places) for every genre, including genres with no shows (`0`, `0`, `NULL`).

## When you're stuck

- **"make a VIEW, not a table"**: you wrote `CREATE TABLE ... AS`. Write `CREATE VIEW ... AS`.
- **`ERROR 1050: Table 'catalogue' already exists`**: use `CREATE OR REPLACE VIEW` to change an existing view.
- **Mwisho wa Reli is missing**: the joins to genres or ratings need to be `LEFT JOIN`s.
- **`ERROR 1369: CHECK OPTION failed`**: that's `WITH CHECK OPTION` doing its job.
- **The genre board says Comedy has 25 shows**: joining the votes made one row per vote. Count `DISTINCT sg.show_id`.
