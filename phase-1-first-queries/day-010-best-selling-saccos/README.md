# Day 10: Best-Selling Saccos

## The brief

The Matatu Owners' Association wants to recognise the busiest saccos of the week, and spot the routes where matatus run full. That means grouping trips (Day 9), then keeping only the *groups* that pass a test: "at least 15 trips", "more than 10,000 bob". `WHERE` can't do that, because it runs before the groups exist. **`HAVING`** filters groups after they're made.

`setup.sql` loads 58 trips from one week in July 2025: date, sacco, route, passengers (a 14-seater carries up to 14) and fare. All made up.

## What you'll use

```sql
SELECT sacco, COUNT(*) AS trips
FROM trips
GROUP BY sacco
HAVING COUNT(*) >= 15;
```

**`WHERE` filters rows; `HAVING` filters groups.** "Trips with 10 or more passengers" is about single rows, so it's `WHERE passengers >= 10`. "Saccos with at least 10 such trips" is about whole groups, so it's `HAVING COUNT(*) >= 10`. One query can use both.

**The order you write a query in is not the order it runs in.** You write:

```
SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT ...
```

MySQL works it out in this order:

1. `FROM`: which table
2. `WHERE`: keep matching rows
3. `GROUP BY`: make the piles
4. `HAVING`: keep matching piles
5. `SELECT`: work out the columns (and their `AS` names)
6. `ORDER BY`: sort
7. `LIMIT`: cut

That's why `WHERE` can't use an aggregate (the piles don't exist yet), and why the standard says `WHERE` and `HAVING` can't use a `SELECT` alias, while `ORDER BY` can. MySQL lets `HAVING` use aliases as a convenience, but writing the aggregate out, as in `HAVING COUNT(*) >= 15`, works in every database. GATE asks about this order often.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS matatu;"
tools/mysql.sh matatu < phase-1-first-queries/day-010-best-selling-saccos/setup.sql
```

1. `starter/0-busy_saccos.sql`: saccos with at least 15 trips: `sacco`, `trips`, most first, ties alphabetical.
2. `starter/1-big_earners.sql`: saccos that took more than 10,000 bob (`passengers * fare_kes`, added up): `sacco`, `revenue`, biggest first.
3. `starter/2-full_routes.sql`: routes averaging at least 9.5 passengers: `route_no`, `avg_passengers` rounded to 1 place, fullest first. Filter on the real average, not the rounded one.
4. `starter/3-full_trips.sql`: each sacco's number of trips with 10 or more passengers (`full_trips`), keeping saccos with at least 10. Alphabetical by sacco.
5. `starter/4-top_two_routes.sql`: leave out Mwananchi Shuttle's trips, keep routes with at least 8 trips, and show the two routes with the most passengers: `route_no`, `passengers`, most first.
6. `pytest phase-1-first-queries/day-010-best-selling-saccos`

## The kata: Shared Routes

In `starter/kata.sql`, list routes run by more than one sacco: `route_no` and `saccos` (how many different saccos), in route order.

## When you're stuck

- **`ERROR 1111: Invalid use of group function`**: an aggregate is in `WHERE`. Move that condition to `HAVING`.
- **Umoja Express appears in the full-trips answer**: it has 14 trips, but only 7 with 10 or more passengers. The passenger filter belongs in `WHERE`, before grouping.
- **The busy-saccos test fails after rows are deleted**: you filtered on a fixed list of names instead of on `COUNT(*)`.
- **Route 42 appears in the top two**: the Mwananchi trips weren't left out first, or the trip-count test went in `WHERE`.
- **The kata counts trips instead of saccos**: `COUNT(DISTINCT sacco)`.
