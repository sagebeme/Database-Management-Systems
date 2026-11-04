# Day 8: Shop Totals

## The brief

Mama Njeri runs a duka in Kayole, and for two weeks in June her nephew Kevin typed every sale into a table: the day, the item, its category, how many, the price, and whether it was cash or M-Pesa. Now she wants numbers, not rows. How many sales? How much money? What's the average price? Cheapest and dearest? How much came in on M-Pesa?

Each answer squeezes many rows into one value. Functions that do that are called **aggregate functions**.

`setup.sql` loads 40 sales. Prices are close to real Nairobi shop prices in 2025; the sales are made up.

## What you'll use

```sql
SELECT COUNT(*) FROM sales;                       -- how many rows
SELECT COUNT(DISTINCT item) FROM sales;           -- how many different items
SELECT SUM(qty * unit_price) FROM sales;          -- add up a calculation, row by row
SELECT AVG(unit_price) FROM sales;                -- the mean
SELECT MIN(unit_price), MAX(unit_price) FROM sales;
SELECT COUNT(*) FROM sales WHERE payment = 'cash';   -- WHERE picks the rows first
```

- `WHERE` runs **before** the aggregate: first choose the rows, then count or add up only those.
- `SUM(qty * unit_price)` works out `qty * unit_price` for each row, then adds the results. That's not the same as `SUM(qty) * SUM(unit_price)`.
- `AVG(unit_price)` is the average price *per sale*, not per item on the shelf: an item sold ten times counts ten times.
- Name your answers with `AS`, or the columns come back called `COUNT(*)` and `SUM(qty * unit_price)`.
- An aggregate with no `GROUP BY` returns exactly one row, even when no rows match (then `COUNT` is `0` and `SUM` is `NULL`). Tomorrow you get one row per group.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS duka;"
tools/mysql.sh duka < phase-1-first-queries/day-008-shop-totals/setup.sql
```

1. `starter/0-count_sales.sql`: how many sales, as `sales`.
2. `starter/1-revenue.sql`: total money taken, as `revenue`.
3. `starter/2-average_price.sql`: average unit price, rounded to 2 places, as `average_price`.
4. `starter/3-cheapest_dearest.sql`: lowest and highest unit price, as `cheapest` and `dearest`.
5. `starter/4-mpesa_takings.sql`: number of M-Pesa sales and their total, as `mpesa_sales` and `mpesa_revenue`.
6. `pytest phase-1-first-queries/day-008-shop-totals`

## The kata: Range Check

In `starter/kata.sql`, print how many *different* items were sold, as `items`. (The shop stocks twelve. One of them never sold.)

## When you're stuck

- **The count test fails after rows are deleted**: you typed the number instead of counting. The tests change the data to catch that.
- **The revenue is far too big**: you multiplied two sums. Multiply inside: `SUM(qty * unit_price)`.
- **The kata says 40**: `COUNT(item)` counts rows that have an item. `COUNT(DISTINCT item)` counts different items.
- **`average_price` has lots of decimals**: wrap it: `ROUND(AVG(unit_price), 2)`.
