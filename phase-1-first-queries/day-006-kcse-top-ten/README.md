# Day 6: KCSE Top Ten

## The brief

Results day. The *Daily Nation* education desk has a table of candidates with their school, county, total points (out of 84) and mean grade, and the editor, Mr Kiprotich, wants lists for tomorrow's paper: everyone ranked, the top ten, the next ten for page two, which counties made the list, and the A students.

A table has no order of its own, so a list in an order you can rely on needs **`ORDER BY`**. Today you sort, cut to size, and remove duplicates.

`setup.sql` loads 25 candidates. The schools are real; the candidates and points are made up.

## What you'll use

```sql
SELECT name, points FROM results ORDER BY points DESC;            -- biggest first
SELECT name, points FROM results ORDER BY points DESC, name ASC;  -- then A to Z among ties
SELECT name FROM results ORDER BY points DESC LIMIT 5;            -- only the first five
SELECT name FROM results ORDER BY points DESC LIMIT 5 OFFSET 5;   -- skip five, then five: 6th to 10th
SELECT DISTINCT county FROM results;                              -- each county once
```

- `ASC` (smallest first, A to Z, the default) or `DESC` (biggest first).
- **Break ties.** Three candidates have 78 points. Sorted only by points, MySQL may list them in any order, and a different order tomorrow. Adding `name` as a second sort key makes the order fixed. Without it, pages (`LIMIT`/`OFFSET`) can show someone twice or skip someone.
- `LIMIT n OFFSET m` skips *m* rows and returns the next *n*. Page *p* of size 10 is `LIMIT 10 OFFSET (p - 1) * 10`.
- `DISTINCT` applies to the whole row you select: `SELECT DISTINCT county, school` gives each county–school pair once.
- `LIMIT` without `ORDER BY` returns *some* rows, not the first ones.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS kcse;"
tools/mysql.sh kcse < phase-1-first-queries/day-006-kcse-top-ten/setup.sql
```

Every list is "best first, ties alphabetical" unless it says otherwise.

1. `starter/0-top_score.sql`: `name` and `points` of everyone.
2. `starter/1-top_ten.sql`: `name`, `school` and `points` of the top ten.
3. `starter/2-next_ten.sql`: `name` and `points` of candidates 11 to 20.
4. `starter/3-counties.sql`: each `county` once, in alphabetical order.
5. `starter/4-a_grades.sql`: `name`, `grade` and `points` of everyone with an A or A-.
6. `pytest phase-1-first-queries/day-006-kcse-top-ten`

## The kata: Runner-Up Score

A classic interview question. In `starter/kata.sql`, print the second-highest number of points anyone got, in a column called `second_best`. If two people tie for the top, the runner-up score is still the next *different* number.

## When you're stuck

- **The tied candidates are in the wrong order**: add `, name` to the `ORDER BY`.
- **The next-ten list starts in the wrong place**: `OFFSET 10` skips ten rows, so it starts at the 11th.
- **`DISTINCT` gives more rows than expected**: you selected more than one column, so it's removing duplicate *pairs*.
- **The kata says 84 when two people have 84**: `SELECT DISTINCT points` before `LIMIT 1 OFFSET 1`.
