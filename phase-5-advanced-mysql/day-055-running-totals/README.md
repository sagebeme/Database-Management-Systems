# Day 55: Running Totals

## The brief

Two kiosks take M-Pesa payments: Kawangware Fresh (closed on Sundays) and Thika Road Duka. The owner looks at a long list of daily takings and asks the questions every shopkeeper asks:

- How much have we taken so far this month?
- Was today better or worse than yesterday?
- Smoothing out the bumps, are we growing?
- Which days fell off a cliff the next day?

Yesterday's window functions ranked rows. Today they look **along** the rows in order: adding up as they go, or peeking at the row before or after.

## What you'll use

```sql
SUM(amount) OVER (PARTITION BY till ORDER BY day)            -- running total
LAG(amount) OVER (PARTITION BY till ORDER BY day)            -- the previous row's amount (NULL on the first)
LEAD(amount) OVER (PARTITION BY till ORDER BY day)           -- the next row's
AVG(amount) OVER (PARTITION BY till ORDER BY day
                  ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)  -- this row and the two before it
```

- **Adding `ORDER BY` inside `OVER` changes what `SUM` means.** Without it, `SUM(amount) OVER (PARTITION BY till)` is the till's grand total on every row. With it, the sum covers the rows *up to this one*: a running total.
- **The frame** says which rows count: `ROWS BETWEEN <start> AND <end>`, where each end is `UNBOUNDED PRECEDING`, `n PRECEDING`, `CURRENT ROW`, `n FOLLOWING` or `UNBOUNDED FOLLOWING`. With `ORDER BY`, the default is "from the start up to the current row, plus any rows tied with it". Ties are why `ROWS` is safer when you mean rows.
- **`LAG` and `LEAD` count rows, not days.** Kawangware Fresh has no Sunday row, so Monday's `LAG` is Saturday. That's usually what you want ("the previous trading day"); if you need the calendar day before, join on `day - INTERVAL 1 DAY` instead.
- `LAG(amount, 7)` looks 7 rows back. `LAG(amount, 1, 0)` gives 0 instead of `NULL` when there's no previous row.
- **Filtering on a window** (like yesterday) needs a derived table.
- **`CHANGE` is a reserved word** in MySQL (it's in `ALTER TABLE ... CHANGE`), so the column is called `vs_previous`.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS tills;"
tools/mysql.sh tills < phase-5-advanced-mysql/day-055-running-totals/setup.sql
```

1. `starter/0-running_total.sql`: each till's takings so far.
2. `starter/1-vs_previous.sql`: today minus the previous trading day.
3. `starter/2-moving_average.sql`: a 3-day moving average, rounded.
4. `starter/3-big_drops.sql`: days followed by a drop of more than 30%.
5. `pytest phase-5-advanced-mysql/day-055-running-totals`

## The kata: Record Days

In `starter/kata.sql`, list the days when a till beat its best day so far (the first day always counts). Equalling the record doesn't count. Think about the frame: the best of every row *before* this one, not counting this one.

## When you're stuck

- **The running total is the same on every row**: there's no `ORDER BY` inside `OVER`.
- **Thika Road Duka's running total starts at 67,400**: add `PARTITION BY till`, or the windows run across both tills.
- **The moving average's first rows are wrong**: there are fewer than 3 rows to average there, and that's fine; `AVG` uses what's in the frame. Check you wrote `2 PRECEDING`, not `3`.
- **`ERROR 1064` near `change`**: it's reserved. Call the column `vs_previous` as asked.
- **The drop list is empty or huge**: a drop of more than 30% means the next day is *below 70%* of today: `next_amount < amount * 0.7`.
- **The kata lists every day**: the frame includes the current row, so `amount > MAX(...)` is never true and `>=` always is. End the frame at `1 PRECEDING`.
