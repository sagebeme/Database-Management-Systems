# Day 74: How Many Pages

## The brief

The SACCO's treasurer asks why finding one member by phone number is instant, but "list everyone who joined in 2019" takes a second, and why the server needs so much RAM. The answer is in how rows sit on disk. A disk doesn't hand out rows; it hands out **blocks** (InnoDB calls them **pages**), and every read costs a whole one. Counting block reads is how database people predict how fast a query will be, and it's on every DBMS exam.

Today you'll do the classic arithmetic by hand and in Python, then ask MySQL how many pages its own tables take.

## What you'll use

- **Block size** `B` and **record size** `R`, in bytes.
- **Blocking factor** `bfr = floor(B / R)`: whole records per block. Records here don't *span* blocks: the left-over bytes at the end of each block are wasted.
- **File blocks** `b = ceil(r / bfr)` for `r` records.

Costs of finding one record, in block reads:

| Method | Needs | Reads |
|---|---|---|
| Linear search | nothing | `b/2` on average for a unique key; `b` otherwise |
| Binary search | file sorted on the key | `ceil(log2 b)` |
| Single-level index | an index file | binary search the index blocks, + 1 data block |
| Multilevel index | an index on the index... | one read per level, + 1 data block |

An **index entry** is a key plus a block pointer, so an index has a much bigger blocking factor than the data: the **fan-out** `fo = floor(B / (V + P))`.

- A **primary index** is on the key the file is sorted by. It needs one entry per *data block* (the first key in each block): a **sparse** index.
- A **secondary index** is on any other field. The file isn't sorted on it, so it needs one entry per *record*: a **dense** index.
- A **clustering index** is on a sorted non-key field: one entry per distinct value.

**Multilevel**: the first level of an index is itself a sorted file, so index *that* with a second level, and so on, until a level fits in one block. Each level has `fo` times fewer blocks, so the number of levels is about `log_fo(entries)`. With `fo` in the hundreds, three or four levels reach millions of rows. That's the idea behind the B+ tree (Day 76).

**A worked example** (the one in most textbooks): `r = 30,000`, `R = 100`, `B = 1,024`, key 9 bytes, pointer 6.

- `bfr = 10`, `b = 3,000`. Linear: 1,500 reads. Binary: `ceil(log2 3000) = 12`.
- Index entries are 15 bytes: `fo = 68`. A primary index has 3,000 entries in `ceil(3000/68) = 45` blocks. Binary search over those is 6 reads, +1 for the data: 7.
- Make it multilevel: 45 blocks, then 1. Two levels, + 1: 3 reads.

**In InnoDB** every page is 16 KB (`innodb_page_size`). The table *is* its primary key's B+ tree (the clustered index, Day 77), so `data_length` in `information_schema.tables` is that tree's size, and `index_length` is the secondary indexes. Both are estimates, updated by `ANALYZE TABLE`.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS pages;"
tools/mysql.sh pages < phase-6-transactions-and-storage/day-074-how-many-pages/setup.sql
```

1. `starter/0-page_size.sql`: InnoDB's page size, as `page_size`.
2. `starter/1-table_sizes.sql`: for every table in the current database, `table_name`, `table_rows`, `data_pages` and `index_pages` (whole pages, with `DIV`). Use `information_schema.tables` and `DATABASE()`, not a typed database name.
3. `starter/blocks.py`: `blocking_factor`, `file_blocks`, `linear_search_blocks`, `binary_search_blocks`, `index_levels`.
4. `starter/answers.py`: the worked example, with your own arithmetic.
5. `pytest phase-6-transactions-and-storage/day-074-how-many-pages`

`loans` has fewer rows than `members` but more pages. Look at its `notes` column and work out why.

## The kata: The Cheapest Way In

In `starter/blocks.py`, write `cheapest_lookup(records, record_size, block_size, key_size, pointer_size, sorted_on_key)`: work out each method that's possible and return `(method, reads)` for the cheapest. Try a few tiny files: at what size does an index stop being worth it?

## When you're stuck

- **`table_name` comes back as `TABLE_NAME`**: `information_schema` columns are upper case in MySQL 8. Give each one an alias.
- **Other databases' tables show up**: filter on `table_schema = DATABASE()`.
- **`data_pages` is a decimal**: `/` divides exactly; `DIV` divides whole numbers.
- **`binary_search_blocks(1024)` gives 11**: `log2(1024)` is exactly 10. Use `math.log2` and `math.ceil`, not `int(...) + 1`.
- **`index_levels` is one too many or too few**: the first level has `ceil(entries / fanout)` blocks. Keep dividing by `fanout` while a level has more than one block; count the levels, not the divisions.
- **The primary index has 3,000 blocks**: a primary index has one entry per *data block*, not per record.
