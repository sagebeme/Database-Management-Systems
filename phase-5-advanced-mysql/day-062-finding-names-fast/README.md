# Day 62: Finding Names Fast

## The brief

Pamoja's user list has grown to 50,000 names, and the orders table to 50,000 rows. Searches that used to be instant now take a moment, and the app runs them thousands of times an hour. With no index, every `WHERE` reads the whole table, every row, to find the few it wants. That's called a **full table scan**.

An **index** is a sorted copy of one or more columns, with a pointer back to each row, so MySQL can jump to what it wants, like the index at the back of a book. Today you build indexes, ask MySQL whether it uses them with `EXPLAIN`, and see why some queries can't use them however hard you try.

## What you'll use

```sql
CREATE INDEX idx_orders_customer ON orders (customer_id);
EXPLAIN SELECT * FROM orders WHERE customer_id = 42;
```

```
+----+-------------+--------+------+---------------------+---------------------+---------+-------+------+-------+
| id | select_type | table  | type | possible_keys       | key                 | key_len | ref   | rows | Extra |
+----+-------------+--------+------+---------------------+---------------------+---------+-------+------+-------+
|  1 | SIMPLE      | orders | ref  | idx_orders_customer | idx_orders_customer | 4       | const |   10 | NULL  |
```

| `EXPLAIN` column | What it tells you |
|---|---|
| `type` | how rows are found: `ALL` (a full scan, the bad one), `range` (a stretch of an index), `ref` (all rows with one value), `const` (one row by primary key) |
| `possible_keys` / `key` | the indexes it could use / the one it chose (`NULL` means none) |
| `rows` | how many rows it expects to read |
| `Extra` | `Using index` (answered from the index alone, without reading the table), `Using where`, `Using temporary`, `Using filesort` |

- **Composite indexes** `(a, b)` are sorted by `a`, then by `b` within each `a`. They help `WHERE a = ?` and `WHERE a = ? AND b > ?`, but not `WHERE b = ?` alone (the **leftmost prefix** rule), like a phone book sorted by surname then first name.
- **Prefix indexes**: `name(1)` indexes only the first character. They're smaller, and good enough for `LIKE 'Z%'`.
- **Sargable** queries can use an index: the column must stand alone on one side. `WHERE YEAR(placed_on) = 2025` hides the column inside a function, so the index (sorted by `placed_on`, not by `YEAR(placed_on)`) can't be used. The same question as a range can: `WHERE placed_on >= '2025-01-01' AND placed_on < '2026-01-01'`. The same goes for `LIKE '%ama'` (no index on the end of a word) and `WHERE price * 1.16 > 1000`.
- **The optimizer may still say no.** If a query wants a large share of the table (all of 2025 here is about a third of it), jumping around the index costs more than one straight scan. `EXPLAIN` will show `ALL` even though the index exists, and that's the right choice.
- **A covering index** holds every column a query needs, so MySQL never reads the table: `Extra: Using index`.
- **Indexes aren't free.** Every insert, update and delete must update every index too, and each one takes disk space. Index what your queries actually filter, join and sort on. The primary key and `UNIQUE` columns already have one each, and so does every foreign key.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS fast;"
tools/mysql.sh fast < phase-5-advanced-mysql/day-062-finding-names-fast/setup.sql
```

Before each step, `EXPLAIN` the query; after it, `EXPLAIN` it again and compare `type`, `key` and `rows`.

1. `starter/0-index_my_names.sql`: `idx_name_first` on the first letter of `name`. Try `SELECT COUNT(*) FROM names WHERE name LIKE 'Z%';`.
2. `starter/1-index_name_score.sql`: `idx_name_first_score` on the first letter and the score.
3. `starter/2-index_customer.sql`: `idx_orders_customer`.
4. `starter/3-june_sales.sql`: `idx_placed_on`, then June 2025's orders and takings, sargably.
5. `pytest phase-5-advanced-mysql/day-062-finding-names-fast`

## The kata: Covering Index

In `starter/kata.sql`, create `idx_customer_report` so that this query never touches the table:

```sql
SELECT customer_id, SUM(total) FROM orders WHERE placed_on >= '2026-01-01' GROUP BY customer_id;
```

Which column must come first, so that the `WHERE` can use the index?

## When you're stuck

- **`ERROR 1061: Duplicate key name 'idx_name_first'`**: it's already there from an earlier try. `DROP INDEX idx_name_first ON names;` and run your file again (or reload `setup.sql`).
- **`key` is `NULL` for June 2025**: the column is inside `YEAR()` or `MONTH()`. Compare `placed_on` itself with a range.
- **Your June totals don't match**: `BETWEEN '2025-06-01' AND '2025-06-30'` works for a `DATE`, but `< '2025-07-01'` is the habit that also works for `DATETIME`s, where 30 June at 3 pm is after `'2025-06-30'`.
- **The kata's `EXPLAIN` doesn't say `Using index`**: the index is missing `customer_id` or `total`.
- **The kata's index isn't chosen**: put `placed_on` first, since the query filters on it.
