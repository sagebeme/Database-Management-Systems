# Day 51: Breaking the Rules on Purpose

## The brief

Ten days of normalising, and now some advice that sounds like the opposite: **sometimes you store a fact twice on purpose.**

A delivery app shows each shop with its number of orders. Counting them every time someone opens the shop list means scanning `orders`, which is fine for 30 orders and slow for 30 million. So the developers added `shops.orders_count`, a copy of a number they could count, and updated it in the app code whenever an order came in. That's **denormalisation**: a redundant copy kept for speed.

Then someone wrote a second way to place orders and forgot the update. Two shops' counts are now wrong, and nothing in the database noticed. That's the price. Today you pay it on purpose and in the open: you build a summary table, refresh it safely, and catch and fix the drift.

## What you'll use

| Kind | Example | Kept fresh by |
|---|---|---|
| **Copied column** | `orders.shop_name` next to `orders.shop_id` | every write that changes the original |
| **Stored count or total** | `shops.orders_count` | every insert and delete on `orders` |
| **Summary table** | `daily_sales (shop_id, day, order_count, revenue)` | a refresh job (now), or a trigger (Day 58) |

- **The rule of thumb**: normalise first. Then denormalise only what a measurement says is slow, and write down which table is the truth and which is the copy.
- **Reads get faster, writes get slower and riskier**: every change has to update the copy too, or it drifts.
- **A view (Day 26) stores nothing.** It's a saved query, run fresh every time. Some databases have *materialised* views that store their rows. MySQL doesn't, so a summary table is how you get one.
- **Safe to re-run**: a refresh that only `INSERT`s doubles everything the second time. Either empty the table first (`DELETE FROM daily_sales;` then insert), or use `INSERT ... ON DUPLICATE KEY UPDATE` (which still misses deleted orders). Re-running must give the same result. That's being **idempotent**.
- **Drift check**: compare the copy with the truth. `LEFT JOIN` so shops with no orders are checked too (Day 20).
- **Fix it in one statement** with a correlated subquery (Day 18):

  ```sql
  UPDATE shops AS s SET orders_count = (SELECT COUNT(*) FROM orders AS o WHERE o.shop_id = s.id);
  ```

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS dukas;"
tools/mysql.sh dukas < phase-4-normalisation/day-051-breaking-the-rules-on-purpose/setup.sql
```

1. `starter/0-daily_sales.sql`: create the summary table and fill it from `orders`.
2. `starter/1-refresh.sql`: bring it up to date. The tests add orders, delete one, and run it twice.
3. `starter/2-drift.sql`: shops whose `orders_count` is wrong: `name`, `stored_count`, `actual_count`.
4. `starter/3-fix_drift.sql`: fix every count in one `UPDATE`.
5. `starter/answers.py`.
6. `pytest phase-4-normalisation/day-051-breaking-the-rules-on-purpose`

## The kata: The Fast Report

In `starter/kata.sql`, each shop's best day (`name`, `day`, `revenue`) from `daily_sales` only; that's the point of having it. Ties go to the earlier day.

## When you're stuck

- **`ERROR 1064` near `stored`**: `STORED` is a keyword in MySQL 8 (generated columns), which is why the columns are `stored_count` and `actual_count`. Backticks also work: `` `stored` ``.
- **Everything doubles after the refresh**: you inserted without emptying the table first.
- **The deleted order's day is still in `daily_sales`**: `ON DUPLICATE KEY UPDATE` only touches rows that come back from the `SELECT`. A day with no orders left never comes back, so delete first.
- **Kitengela Hardware is missing from the drift list**: it has no orders, so an inner join drops it. Use `LEFT JOIN` and `COUNT(o.id)`.
- **`ERROR 1093: You can't specify target table 'shops' for update in FROM clause`**: the subquery should read `orders`, not `shops`.
- **The kata's ties come out on the later day**: sort by `revenue DESC, day` inside the subquery.
