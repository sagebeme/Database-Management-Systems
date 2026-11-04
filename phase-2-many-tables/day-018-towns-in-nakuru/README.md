# Day 18: Towns in Nakuru

## The brief

The delivery startup's dispatcher, Wambui, asks questions that need two steps: "Which towns are in Nakuru?" means first finding Nakuru's id in `counties`, then the towns with that `county_id`. "Which shops sell more than average?" means first working out the average. You could run the first step, copy the answer, and paste it into the second. A **subquery** does both in one statement: a `SELECT` inside another, whose result the outer query uses.

`setup.sql` loads the counties and towns from Day 17 (plus Gilgil and Nairobi) and 18 shops on the app's books, with their monthly sales (made up).

## What you'll use

**A subquery that returns one value** can go wherever a value can:

```sql
SELECT name FROM towns
WHERE county_id = (SELECT id FROM counties WHERE name = 'Kiambu');

SELECT name, monthly_sales FROM shops
WHERE monthly_sales > (SELECT AVG(monthly_sales) FROM shops);
```

If it returns more than one row, `=` fails with `Subquery returns more than 1 row`.

**A subquery that returns a list** goes with `IN` or `NOT IN`:

```sql
SELECT name FROM counties
WHERE id IN (SELECT county_id FROM towns WHERE name LIKE 'M%');
```

Subqueries can nest: shops in towns in a county is two levels deep.

**A correlated subquery** refers to the outer query's current row, so it's worked out again for each row:

```sql
SELECT town_id, name, monthly_sales
FROM shops AS s
WHERE monthly_sales = (SELECT MAX(monthly_sales) FROM shops WHERE town_id = s.town_id);
```

For each shop `s`, the inner query finds the best sales *in that shop's town*. The alias `s` is how the inner query tells the outer table apart from its own.

**A subquery in `FROM`** (a *derived table*) is a temporary table you can query again. It must have an alias:

```sql
SELECT MAX(total) FROM (SELECT town_id, SUM(monthly_sales) AS total FROM shops GROUP BY town_id) AS t;
```

That's how you take an aggregate of aggregates: `AVG(SUM(...))` isn't allowed directly.

**Careful with `NOT IN` and `NULL`.** If the subquery's list contains a `NULL`, `x NOT IN (...)` is never true (Day 11's three-valued logic), and you get no rows at all. `shops.town_id` is `NOT NULL`, so today is safe. Day 22 shows the trap, and `NOT EXISTS`, which avoids it.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS places;"
tools/mysql.sh places < phase-2-many-tables/day-018-towns-in-nakuru/setup.sql
```

Look things up by name; don't type ids. The tests rename counties to catch typed ids.

1. `starter/0-towns_in_nakuru.sql`: `id`, `name` of towns in Nakuru, in id order.
2. `starter/1-shops_in_kiambu.sql`: `name` of shops in Kiambu county, alphabetical.
3. `starter/2-above_average.sql`: `name`, `monthly_sales` of shops above the average, biggest first.
4. `starter/3-towns_without_shops.sql`: `name` of towns with no shop, alphabetical.
5. `starter/4-top_shop_per_town.sql`: for each town with shops, `town_id`, and the `name` and `monthly_sales` of its best shop, in town order.
6. `pytest phase-2-many-tables/day-018-towns-in-nakuru`

## The kata: The Average Town

In `starter/kata.sql`, add up each town's shop sales, then average those totals over the towns that have shops. Print it rounded to a whole number as `avg_town_sales`.

## When you're stuck

- **`ERROR 1242: Subquery returns more than 1 row`**: use `IN`, not `=`, when the inner query can return several rows.
- **`ERROR 1248: Every derived table must have its own alias`**: add `AS t` after the bracket.
- **`ERROR 1111: Invalid use of group function`**: `AVG(SUM(...))` isn't allowed. Sum in a derived table, then average outside.
- **The best-shop query returns one shop for everyone**: the inner query needs `WHERE town_id = s.town_id`, and the outer table needs the alias `s`.
- **Towns without shops comes back empty**: check you used `NOT IN (SELECT town_id FROM shops)`, not `NOT IN (SELECT id FROM shops)`.
