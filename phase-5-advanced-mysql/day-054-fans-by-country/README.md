# Day 54: Fans by Country

## The brief

A streaming app wants a chart page: the biggest acts overall, the top two in each genre, and each act's share of its country's fans. `GROUP BY` can't do it, because it squashes the rows: you get one row per genre and lose the artists. You want every artist's row **and** something worked out across a group of rows.

That's a **window function**. It looks at a "window" of rows related to the current one, but leaves every row in the result.

## What you'll use

```sql
SELECT name, genre, fans,
       RANK() OVER (ORDER BY fans DESC)                         AS overall,
       DENSE_RANK() OVER (PARTITION BY genre ORDER BY fans DESC) AS in_genre,
       SUM(fans) OVER (PARTITION BY genre)                      AS genre_total
FROM artists;
```

- **`OVER (...)`** turns a function into a window function. Empty brackets mean "all rows".
- **`PARTITION BY genre`** restarts the window for each genre, like `GROUP BY` but without squashing.
- **`ORDER BY fans DESC`** inside `OVER` decides the ranking order. It has nothing to do with the query's final `ORDER BY`, so you still need that.

| Function | Two artists tied at 760,000 for 2nd | Next one |
|---|---|---|
| `ROW_NUMBER()` | 2 and 3 (an arbitrary pick, unless you add a tiebreak) | 4 |
| `RANK()` | 2 and 2 | 4 (skips) |
| `DENSE_RANK()` | 2 and 2 | 3 (no gap) |

- **Aggregates as windows**: `SUM(fans) OVER (PARTITION BY origin)` puts the country total on every row, so `100 * fans / SUM(fans) OVER (PARTITION BY origin)` is each act's share.
- **You can't filter on a window function in `WHERE`**: `WHERE ROW_NUMBER() OVER (...) <= 2` fails, because `WHERE` runs before windows are worked out. Put the window in a derived table (Day 18) and filter outside.
- **A window over a `GROUP BY`**: windows run *after* grouping, so `DENSE_RANK() OVER (ORDER BY SUM(fans) DESC)` ranks the groups.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS music;"
tools/mysql.sh music < phase-5-advanced-mysql/day-054-fans-by-country/setup.sql
```

1. `starter/0-fans_by_origin.sql`: a warm-up, plain `GROUP BY`.
2. `starter/1-rank_artists.sql`: overall place, ties sharing a place.
3. `starter/2-rank_within_genre.sql`: rank within each genre, no gaps.
4. `starter/3-top_two_per_genre.sql`: exactly two per genre.
5. `starter/4-share_of_country.sql`: each act's percentage of its country's fans.
6. `pytest phase-5-advanced-mysql/day-054-fans-by-country`

## The kata: Second Best Country

In `starter/kata.sql`, find the origin with the second-highest total fans (all of them, if tied): `origin`, `nb_fans`. The tests make two countries tie for first. Which ranking function still finds a "second"?

## When you're stuck

- **`ERROR 3593: You cannot use the window function 'row_number' in this context`**: you put it in `WHERE`. Wrap the query in `(...) AS ranked` and filter outside.
- **Bongo Flava shows three acts in the top two**: you used `RANK` or `DENSE_RANK`, which keep ties. `ROW_NUMBER()` with `ORDER BY fans DESC, name` gives exactly two.
- **The ranks look right but the rows come out jumbled**: the `ORDER BY` inside `OVER` doesn't sort the result. Add one at the end.
- **The percentages are tiny, or all 100.0**: tiny means `OVER ()`, the grand total of every country. All 100.0 means a `GROUP BY name` crept in, so each sum is just the artist's own fans. You want `OVER (PARTITION BY origin)` and no `GROUP BY`.
- **The kata returns nothing after the shake-up**: `RANK` jumps from 1 to 3 after a tie for first. Use `DENSE_RANK`.
