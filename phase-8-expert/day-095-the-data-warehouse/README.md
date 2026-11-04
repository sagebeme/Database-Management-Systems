# Day 95: The Data Warehouse

## The brief

A chain of six dukas runs on a shop system built for selling: insert a sale, look up a price, fast, all day. Then the owner asks, "Which counties make the most from oil, and how much of our bakery money comes in at weekends?" Questions like that read millions of rows, join everything and group by everything, and they slow down the tills while they run.

So businesses keep two kinds of database. **OLTP** (online transaction processing) runs the business: many small reads and writes, normalised (Phase 4). **OLAP** (online analytical processing) answers questions about the business: few, huge reads, shaped for easy analysis. Data flows from one to the other through **ETL**: extract, transform, load. Today you'll build a small warehouse in the classic shape, the **star schema**.

## What you'll use

**A star schema**: one **fact** table in the middle, holding the measurements (one row per sale: quantity, revenue), surrounded by **dimension** tables describing them (when, where, what).

```
              dim_date
                 |
  dim_shop --- fact_sales --- dim_product
```

- Dimensions are deliberately *de*normalised: `dim_date` repeats month, quarter and weekday for every day so nobody has to compute them in a query.
- Dimensions get their own **surrogate keys** (`shop_key`), separate from the shop system's ids. That lets one shop have several rows over time (the kata).
- `date_key` like `20260315` is readable and sorts correctly.
- Analysts then write the same simple shape every time: join the fact to the dimensions they need, filter, group.

**Building a calendar** with `generate_series(DATE '2026-01-01', DATE '2026-12-31', INTERVAL '1 day')`, `extract(quarter FROM d)`, `extract(isodow FROM d)` (Monday 1 to Sunday 7) and `to_char(d, 'YYYYMMDD')`. `to_char(d, 'Day')` pads the name with spaces: `trim` it.

**Subtotals in one query**:

```sql
GROUP BY ROLLUP (county, category)
```

gives a row per county and category, a subtotal per county (category `NULL`), and a grand total (both `NULL`). `CUBE` gives every combination; `GROUPING SETS` lets you list the ones you want. `ORDER BY ... NULLS LAST` puts the totals after their groups.

**Shares**: `sum(revenue) FILTER (WHERE is_weekend)` sums only the weekend rows. Divide by the full sum, times `100.0` (so it isn't whole-number division).

**Slowly changing dimensions**: Ngara Stores moves from Nairobi to Kiambu. Overwrite the county (type 1) and last year's Nairobi sales suddenly count as Kiambu's. **Type 2** keeps history instead: close the old row (`valid_to`, `is_current = false`) and add a new current one. Old facts keep pointing at the old row; new facts point at the new one.

## Steps

```bash
tools/psql.sh postgres -c "CREATE DATABASE warehouse;"
tools/psql.sh warehouse -f phase-8-expert/day-095-the-data-warehouse/setup.sql
```

1. `starter/0-star.sql`: the four tables.
2. `starter/1-etl.sql`: fill them from `shops`, `products` and `sales`.
3. `starter/2-rollup.sql` and `starter/3-weekends.sql`: the owner's questions.
4. `pytest phase-8-expert/day-095-the-data-warehouse`

## The kata: Ngara Stores Moves

In `starter/kata.sql`, write the type 2 update: for every shop whose current dimension row no longer matches the shop system, close the old row and add a new one. Running it twice must change nothing the second time.

## When you're stuck

- **`weekday` is `'Sunday   '`**: `to_char(..., 'Day')` pads to nine characters. `trim(...)`.
- **The fact table has 6,000 rows**: a join to `dim_shop` matched two rows for a shop. Join on `shop_id` *and* `is_current`.
- **Revenue doesn't match the shop system**: revenue is `qty * price`, with the price from `products`.
- **The rollup's totals come first**: `ORDER BY county NULLS LAST, category NULLS LAST`.
- **Weekend share is 0 or 100**: integer division. Multiply by `100.0` first.
- **The kata adds rows for shops that didn't change**: compare name and county with `IS DISTINCT FROM`, and only for the current row.
- **The kata's new rows don't know which shops changed**: an `UPDATE ... RETURNING` inside a `WITH` hands its rows to the `INSERT` that follows.
