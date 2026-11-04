# Day 4: Matatu Stages

## The brief

Brian is building a matatu app for people new to Nairobi. The data is a table of routes out of town: where each one goes, which sacco runs it, the fare, the distance, and the night fare (empty when there's no night service). Users ask questions like "what can I get for 70 bob?", and each question is a `SELECT` with a **`WHERE`** clause that keeps only the rows that match.

`setup.sql` loads twelve routes. The destinations are real; the numbers, saccos and fares are made up.

```
+----+----------+-------------+-------------------+----------+-------------+----------------+
| id | route_no | destination | sacco             | fare_kes | distance_km | night_fare_kes |
+----+----------+-------------+-------------------+----------+-------------+----------------+
|  1 | 11       | Ngong       | Neema Line        |      100 |        22.0 |            150 |
|  4 | 25       | Rongai      | Neema Line        |      100 |        18.5 |           NULL |
|  9 | 45       | Westlands   | Umoja Express     |       40 |         4.5 |           NULL |
...
```

## What you'll use

```sql
SELECT route_no, fare_kes FROM routes WHERE fare_kes < 100;
SELECT * FROM routes WHERE destination = 'Thika';
SELECT * FROM routes WHERE sacco <> 'Kasi Sacco';      -- != works too
SELECT * FROM routes WHERE night_fare_kes IS NULL;     -- no value at all
SELECT * FROM routes WHERE night_fare_kes IS NOT NULL;
```

- Comparison operators: `=`, `<>` (or `!=`), `<`, `<=`, `>`, `>=`. They work on numbers, text and dates.
- **`NULL` means "no value"**, not zero and not empty text. Nothing equals `NULL`, not even `NULL`: `night_fare_kes = NULL` is never true, so it returns no rows at all. Use `IS NULL` and `IS NOT NULL`. Day 11 is all about this.
- In MySQL, `=` on text ignores case by default: `'ngong' = 'Ngong'` is true. Day 13 explains why (collations).
- **Read "more than" carefully.** "Longer than 20 km" is `> 20`; "20 km or more" is `>= 20`. Off-by-one at the edges is how most real `WHERE` bugs happen, so the tests add a route of exactly 20 km.
- `ROUND(x, 2)` rounds to two decimal places.

The rows come back in whatever order MySQL finds convenient; you'll choose the order on Day 6.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS matatu;"
tools/mysql.sh matatu < phase-1-first-queries/day-004-matatu-stages/setup.sql
```

1. `starter/0-cheap_routes.sql`: `route_no` and `fare_kes` of routes costing 70 bob or less.
2. `starter/1-to_ngong.sql`: every column of the routes to Ngong.
3. `starter/2-not_neema.sql`: `route_no` and `sacco` of routes not run by Neema Line.
4. `starter/3-no_night_service.sql`: `route_no` and `destination` of routes with no night fare.
5. `starter/4-long_routes.sql`: `route_no` and `distance_km` of routes longer than 20 km.
6. `pytest phase-1-first-queries/day-004-matatu-stages`

## The kata: Shillings per Kilometre

Which routes charge more than 5 bob a kilometre? In `starter/kata.sql`, print `route_no` and the fare per km rounded to 2 decimal places, in a column called `per_km`, for those routes only. (Compare the unrounded value.)

## When you're stuck

- **No rows for the night-fare question**: you wrote `= NULL`. Use `IS NULL`.
- **`ERROR 1054: Unknown column 'Ngong'`**: text needs single quotes: `'Ngong'`.
- **Route 60 shows up in the long-routes test**: `>` not `>=`.
- **The kata has an extra route**: filter on `fare_kes / distance_km > 5`, not on the rounded number. Rounding first turns 5.004 into 5.00 and 4.996 into 5.00, which changes the answer at the edge.
