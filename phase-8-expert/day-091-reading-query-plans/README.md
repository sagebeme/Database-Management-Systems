# Day 91: Reading Query Plans

## The brief

An online duka's county sales report takes four seconds and the owner wants it instant. Guessing ("add an index?") is how juniors fix slow queries. Seniors ask the database what it's actually doing. Every SQL database turns your query into a **plan**, a tree of steps: scan this table, use that index, join these two with this algorithm, sort, aggregate. `EXPLAIN` shows the plan; `EXPLAIN ANALYZE` runs the query and shows what really happened.

Today you'll read Postgres plans, change one with an index, and write the three join algorithms that appear in every plan (and every exam) yourself.

## What you'll use

```sql
EXPLAIN SELECT ...;                     -- the plan, with the planner's cost estimates; doesn't run the query
EXPLAIN ANALYZE SELECT ...;             -- runs it, and adds actual rows and times
EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF, SUMMARY OFF) SELECT ...;   -- just the shape and the real row counts
```

Read a plan from the **innermost, most indented** lines outwards: those run first and feed the lines above them.

```
 Sort (actual rows=8 loops=1)
   ->  HashAggregate (actual rows=8 loops=1)
         ->  Hash Join (actual rows=60000 loops=1)
               Hash Cond: (o.customer_id = c.id)
               ->  Seq Scan on orders o (actual rows=60000 loops=1)
               ->  Hash (actual rows=5000 loops=1)
                     ->  Seq Scan on customers c (actual rows=5000 loops=1)
```

| Node | Means |
|---|---|
| `Seq Scan` | read the whole table |
| `Index Scan` / `Index Only Scan` | walk an index (Days 75 to 77), then fetch rows, or not |
| `Bitmap Index Scan` + `Bitmap Heap Scan` | collect matching row locations from the index, then read those pages in order |
| `Nested Loop` | for each outer row, look up matching inner rows; great when the outer side is small and the inner side has an index |
| `Hash Join` | build a hash table from the smaller input (the `Hash` node), then probe it with each row of the bigger; equality joins only |
| `Merge Join` | both inputs sorted on the join key, walked together like a zip; good when they come sorted already, from an index |
| `Sort`, `HashAggregate`, `GroupAggregate`, `Limit` | what they say |

A big gap between the planner's estimated rows and the actual rows means its statistics are off: `ANALYZE table;` refreshes them.

**The algorithms**, for joining r and s on a key:

- **Nested loop**: compare every pair, `|r| × |s|` comparisons. On disk, the **block nested loop** reads r in chunks that fill memory, and reads s once per chunk: `b_r + ⌈b_r / (M − 2)⌉ × b_s` block reads with `M` buffer pages (one page for s, one for output).
- **Hash join**: one pass to build, one to probe: about `|r| + |s|`.
- **Sort-merge join**: sort both (unless they're sorted already), then one pass over each.

## Steps

```bash
tools/psql.sh postgres -c "CREATE DATABASE plans;"
tools/psql.sh plans -f phase-8-expert/day-091-reading-query-plans/setup.sql
```

1. Run `EXPLAIN (COSTS OFF) SELECT * FROM orders WHERE customer_id = 42;`. Then `starter/0-orders_index.sql`: the index that changes that plan. Run it again.
2. `starter/1-explain.sql`: the county report under `EXPLAIN (ANALYZE, ...)`.
3. `starter/answers.py`: read the join nodes off real plans. The tests run the same plans and check your reading.
4. `starter/joins.py`: `nested_loop_join`, `hash_join`, `block_nested_loop_cost`.
5. `pytest phase-8-expert/day-091-reading-query-plans`

## The kata: Sort-Merge Join

In `starter/joins.py`, write `sort_merge_join`. The hard part is a key that repeats on both sides: every r row with that key joins every s row with it, and then both sides move past it.

## When you're stuck

- **The plan still says `Seq Scan on orders`**: check the index is on `orders (customer_id)`, and that you ran `0-orders_index.sql` in the same database.
- **"turn off COSTS and TIMING"**: the options go in brackets right after `EXPLAIN`: `EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF, SUMMARY OFF) SELECT ...`.
- **Your `ONE_CUSTOMER_JOIN` answer is wrong**: run that `EXPLAIN` *after* creating the index. The plan changes.
- **`hash_join` matches `None` keys**: in SQL, `NULL = NULL` isn't true, so rows with no key never join. Skip them when building and probing.
- **The kata misses pairs when a key repeats**: find the whole run of equal keys on *both* sides, join every pair in the two runs, then move both past them.
- **`work` is too big in the kata**: count each step forward in r or s once; don't go back.
