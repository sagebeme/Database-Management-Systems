# Day 19: Town, County

## The brief

Wambui the dispatcher is tired of seeing `county_id = 5` on her screen. She wants "Naivasha, Nakuru". Splitting data into tables (Day 15) keeps each fact once; a **join** puts the pieces back together for reading, matching each town to its county by the foreign key.

Same data as Day 18: counties, towns and shops.

## What you'll use

```sql
SELECT towns.name, counties.name
FROM towns
JOIN counties ON towns.county_id = counties.id;
```

For every pair of rows, one from each table, `JOIN ... ON` keeps the pairs where the condition is true. Each town matches exactly one county, so you get one row per town with its county's columns alongside.

- **`JOIN` and `INNER JOIN` are the same.** "Inner" means rows with no match on the other side are left out: a town with no shops disappears from a towns–shops join. Tomorrow's outer joins keep them.
- **Aliases** make joins readable: `FROM shops AS s JOIN towns AS t ON s.town_id = t.id`. Once a table has an alias, use it.
- **Same column name in both tables?** Say which one: `towns.name`, `counties.name`. Otherwise you get `Column 'name' in field list is ambiguous`. Name the results with `AS town`, `AS county`.
- **More tables, more joins**: shop → town → county is two `JOIN`s, one per foreign key you follow.
- **Joins and `GROUP BY` mix**: join first, then group the joined rows. Group by the county's id as well as its name, in case two counties ever share a name.
- **A table can join itself** (a *self-join*). Give it two aliases and treat them as two tables: `FROM towns AS a JOIN towns AS b ON a.county_id = b.county_id`.

**Older syntax you'll see**: `FROM towns, counties WHERE towns.county_id = counties.id` means the same as the `JOIN`. And `NATURAL JOIN` joins on *every* column with the same name in both tables. Here that's `id` and `name`, so `towns NATURAL JOIN counties` matches a town to the county with the same id *and* the same name, which is nonsense. Write the `ON` yourself.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS places;"
tools/mysql.sh places < phase-2-many-tables/day-019-town-county/setup.sql
```

1. `starter/0-towns_and_counties.sql`: every town's `id`, `town` and `county`, in town id order.
2. `starter/1-shops_and_towns.sql`: every `shop`, its `town` and `monthly_sales`, biggest first.
3. `starter/2-shops_towns_counties.sql`: `shop`, `town`, `county`, ordered by county, then shop.
4. `starter/3-sales_per_county.sql`: each `county` and its shops' total `sales`, biggest first.
5. `starter/4-neighbours_of_naivasha.sql`: the other towns in Naivasha's county, `name`, alphabetical. Use a self-join, and look Naivasha's county up through the join rather than typing it.
6. `pytest phase-2-many-tables/day-019-town-county`

## The kata: Same Name

In `starter/kata.sql`, list the towns that share their county's name: `town`, alphabetical.

## When you're stuck

- **`Column 'name' in field list is ambiguous`**: prefix it with the table or alias.
- **Far too many rows**: the `ON` condition is missing or wrong, so every town paired with every county (that's a *cross join*: 15 × 7 = 105 rows).
- **Naivasha is in its own neighbour list**: add `AND other.id <> naivasha.id`.
- **The neighbours test fails after Naivasha moves county**: you typed `county_id = 5`. Find it through the join.
- **Athi River is missing from the shops join**: it has no shops, and an inner join leaves out unmatched rows. That's tomorrow.
