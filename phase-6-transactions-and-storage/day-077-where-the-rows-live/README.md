# Day 77: Where the Rows Live

## The brief

You've built a B+ tree by hand. Now look inside MySQL's. In InnoDB, a table doesn't have a B+ tree beside it: the table **is** a B+ tree, sorted by its primary key, with whole rows in the leaves. That's the **clustered index**. Every other index is a **secondary index**: a separate B+ tree whose leaves hold the indexed columns plus the row's *primary key*, not the row.

That one design decision explains a lot of everyday MySQL advice: why lookups by primary key are fastest, why a short primary key matters, why random UUID keys slow inserts down, and why adding one column to an index can make a slow query instant. The SACCO's members table is today's patient.

## What you'll use

**The clustered index** is called `PRIMARY`. Its leaves hold whole rows in primary-key order. A table with no primary key gets the first `UNIQUE` index whose columns are all `NOT NULL`, and if there isn't one, a hidden 6-byte row id in an index called `GEN_CLUST_INDEX`. There's only ever one clustered index, because rows can only be stored in one order.

**A secondary index** (`CREATE INDEX`, `UNIQUE`) has leaves of `(indexed columns, primary key)`. Finding a whole row through it searches *two* trees: the secondary index gives the primary key, and the clustered index gives the row. So:

- A long primary key (a 36-character UUID string, say) is copied into every secondary index and makes them all bigger.
- Random primary keys insert all over the clustered index, splitting pages everywhere and leaving them half full. Increasing keys (`AUTO_INCREMENT`) always add at the right-hand end.

**A covering index** holds every column a query needs, so MySQL never opens the clustered index. `EXPLAIN` says **`Using index`** in `Extra`. Because the primary key is in every secondary leaf, it comes free: an index on `(phone)` covers `SELECT id, phone ... WHERE phone = ?`.

**Column order matters.** An index on `(county, savings)` is sorted by county, then by savings within each county. It helps `WHERE county = ?`, `WHERE county = ? ORDER BY savings` and `GROUP BY county`, but not `WHERE savings > ?` on its own.

**Reading `EXPLAIN`**:

| Column | Look for |
|---|---|
| `type` | `const` (one row by a unique key), `ref`, `range`, `index` (the whole index), `ALL` (the whole table) |
| `key` | the index it chose |
| `rows` | its estimate of rows to read |
| `Extra` | `Using index` (covering), `Using filesort` (it had to sort), `Backward index scan` |

`mysql.innodb_index_stats` holds each index's statistics, including `size`, its pages.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS clustered;"
tools/mysql.sh clustered < phase-6-transactions-and-storage/day-077-where-the-rows-live/setup.sql
```

Run `EXPLAIN` on each query before and after you add each index.

1. `starter/0-unique_phone.sql`: a unique index `uq_phone` on `phone`.
2. `starter/1-find_member.sql`: the `id` and `phone` of the member with phone `254700007919`, answered from `uq_phone` alone.
3. `starter/2-county_index.sql`: an index `idx_county_savings` that covers the county report in the file.
4. `starter/3-index_pages.sql`: each index's `index_name` and `pages`.
5. `starter/answers.py`. Two of the answers you can look up in `mysql.innodb_index_stats` (make a table with no key and `ANALYZE` it).
6. `pytest phase-6-transactions-and-storage/day-077-where-the-rows-live`

Compare the pages: `PRIMARY` holds whole rows; the others hold a column or two plus `id`.

## The kata: Top Savers

In `starter/kata.sql`, create one index, `idx_top_savers`, so that the top ten savers in Nairobi need no sort and no visit to the table's rows. `EXPLAIN` should show it, with `Using index` and no `Using filesort`.

## When you're stuck

- **`ERROR 1062: Duplicate entry`** while creating `uq_phone`: a phone appears twice. It shouldn't with `setup.sql`; reload it.
- **`find_member` doesn't say `Using index`**: you selected a column that isn't in `uq_phone` or the primary key, like `name`. Then MySQL has to fetch the row.
- **The county report says `Using index` but uses another index**: drop the extra index you made while experimenting, or reload `setup.sql`.
- **`3-index_pages.sql` returns nothing**: filter on `database_name = DATABASE()`, `table_name = 'members'`, `stat_name = 'size'`. If the numbers look old, `ANALYZE TABLE members;`.
- **The kata still says `Using filesort`**: the index must put `county` first and `savings` second, so rows for one county are already in savings order. `DESC` is fine: MySQL reads the index backwards.
- **The kata still isn't `Using index`**: `name` must be in the index too. (`id` is there already.)
