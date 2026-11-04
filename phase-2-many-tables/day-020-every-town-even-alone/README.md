# Day 20: Every Town, Even Alone

## The brief

The startup's sales team wants a list of every town and its shops, so they know where to recruit more. Yesterday's inner join had a gap: Athi River, Kikuyu and Maseno have no shops, so they vanished from the list, and those are exactly the towns sales cares about. Ops has a second list: every driver and their home town, including drivers whose town was never filled in.

**Outer joins** keep rows that have no match on the other side, filling the missing columns with `NULL`.

Same places as before, plus Turkana (a county with no towns on the list yet) and seven drivers, two with no home town.

## What you'll use

```sql
SELECT t.name AS town, s.name AS shop
FROM towns AS t
LEFT JOIN shops AS s ON s.town_id = t.id;
```

```
+------------+-------------------+
| town       | shop              |
+------------+-------------------+
| Athi River | NULL              |   <- kept, though it has no shop
| Eldoret    | Eldoret Grains    |
...
```

| Join | Keeps |
|---|---|
| `JOIN` / `INNER JOIN` | only pairs that match |
| `LEFT JOIN` | every row of the left table, matched or not |
| `RIGHT JOIN` | every row of the right table |
| `FULL OUTER JOIN` | every row of both (MySQL doesn't have it; see below) |

- `A RIGHT JOIN B` is `B LEFT JOIN A` with the tables swapped. Most people write `LEFT JOIN` everywhere and put the table they want to keep first.
- **Counting with an outer join**: `COUNT(*)` counts the padded row too, so a town with no shops counts 1. `COUNT(s.id)` counts only real shops (skipping the `NULL`), so it counts 0.
- **Finding rows with no match** (an *anti-join*): `LEFT JOIN`, then keep rows where the right side is `NULL`: `WHERE s.id IS NULL`. Test a column that can't be `NULL` in a real match, like the key.
- **Where you put a condition matters.** A condition on the right table belongs in `ON` if you want to keep unmatched rows: `LEFT JOIN shops s ON s.town_id = t.id AND s.monthly_sales > 200000` keeps every town. Put the same condition in `WHERE` and it throws out the `NULL` rows, turning your outer join back into an inner one.
- **A full outer join in MySQL**: combine a left join and a right join with `UNION`, which also removes the rows they have in common:

  ```sql
  SELECT ... FROM a LEFT JOIN b ON ...
  UNION
  SELECT ... FROM a RIGHT JOIN b ON ...;
  ```

  `UNION` needs the same number of columns in each `SELECT`, and takes column names from the first. An `ORDER BY` at the end sorts the combined result. (`UNION ALL` keeps duplicates.)

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS places;"
tools/mysql.sh places < phase-2-many-tables/day-020-every-town-even-alone/setup.sql
```

1. `starter/0-towns_and_their_shops.sql`: every town with each of its shops: `town`, `shop` (`NULL` if none). Ordered by town, then shop.
2. `starter/1-shop_counts.sql`: every `town` and its number of `shops`, including zero. Most first, ties alphabetical.
3. `starter/2-towns_without_shops.sql`: towns with no shops, with a join this time (no subquery): `town`, alphabetical.
4. `starter/3-right_join.sql`: the same answer as step 2, with `shops` on the left and a `RIGHT JOIN`.
5. `starter/4-towns_and_drivers.sql`: every town and every driver: `town`, `driver`, with `NULL` where there's no match. Towns alphabetical, drivers with no town at the end, drivers alphabetical within each.
6. `pytest phase-2-many-tables/day-020-every-town-even-alone`

## The kata: Empty Counties

In `starter/kata.sql`, list counties with no towns on the list: `county`, alphabetical.

## When you're stuck

- **Towns with no shops show 1**: you counted `*`. Count `s.id`.
- **The towns-without-shops list is empty**: test the right table's key (`s.id IS NULL`), and make sure it's a `LEFT JOIN`.
- **The driver list is missing Lucy and Joy**: a left join from `towns` can't see drivers with no town. That's what the `RIGHT JOIN` half of the `UNION` is for.
- **Mombasa appears twice with the same driver**: you used `UNION ALL`. `UNION` removes the duplicate rows.
- **`ERROR 1222: The used SELECT statements have a different number of columns`**: both halves of a `UNION` must select the same columns.
- **The drivers with no town come first**: MySQL sorts `NULL` first. Sort by `town IS NULL` before `town` (Day 11).
