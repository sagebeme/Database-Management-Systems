# Day 9: Sales by Category

## The brief

Yesterday's totals told Mama Njeri how much she sold. Now she wants it broken down: food against household goods, cash against M-Pesa, Monday against Tuesday, and which items move fastest. Each of those is the same aggregate, worked out separately for each group of rows, which is what **`GROUP BY`** does.

Same data as Day 8: 40 sales at the duka in Kayole.

## What you'll use

```sql
SELECT category, COUNT(*) AS sales
FROM sales
GROUP BY category;
```

```
+-----------+-------+
| category  | sales |
+-----------+-------+
| Food      |    19 |
| Household |     7 |
| ...       |   ... |
```

`GROUP BY category` sorts the rows into piles, one per category, and the aggregate runs once per pile. You get one row out per group.

- **Every column you select must be either in the `GROUP BY` or inside an aggregate.** `SELECT category, item, COUNT(*) ... GROUP BY category` makes no sense (which item, out of a whole pile?) and MySQL rejects it with `ERROR 1055 ... isn't in GROUP BY`.
- You can group by more than one column: `GROUP BY category, payment` makes one group per pair.
- You can `ORDER BY` an aggregate's alias: `ORDER BY sales DESC`.
- `WHERE` still runs before grouping, so `WHERE payment = 'mpesa' GROUP BY category` gives M-Pesa sales per category.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS duka;"
tools/mysql.sh duka < phase-1-first-queries/day-009-sales-by-category/setup.sql
```

1. `starter/0-sales_per_category.sql`: `category` and its number of sales (`sales`), most first, ties alphabetical.
2. `starter/1-revenue_per_category.sql`: `category` and its money (`revenue`), biggest first.
3. `starter/2-daily_takings.sql`: `sold_on` and that day's money (`takings`), in date order.
4. `starter/3-payment_split.sql`: `payment`, `sales` and `revenue`, alphabetical by payment.
5. `starter/4-best_sellers.sql`: the three items that sold the most *units*: `item` and `units` (the total `qty`), most first, ties alphabetical.
6. `pytest phase-1-first-queries/day-009-sales-by-category`

## The kata: Busiest Day

In `starter/kata.sql`, print the single day with the biggest takings: `sold_on` and `takings`.

## When you're stuck

- **`ERROR 1055 ... isn't in GROUP BY`**: a selected column is neither grouped nor aggregated.
- **Every count is 1**: you grouped by `id` or by too many columns, so each group is a single row.
- **Best sellers ranked by number of sales**: units means `SUM(qty)`, not `COUNT(*)`. Someone buying five bars of soap is one sale and five units.
- **Daily takings come out in a strange order**: add `ORDER BY sold_on`. Grouping doesn't promise any order.
