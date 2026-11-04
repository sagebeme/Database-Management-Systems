# Day 92: Too Big for One Table

## The brief

A paybill takes thousands of payments a day. After three years the `payments` table has hundreds of millions of rows: indexes no longer fit in memory, `VACUUM` takes hours, and deleting old data means a `DELETE` that locks and churns for a whole night. Two ideas carry databases past this point:

- **Partitioning** splits one table into many smaller tables *inside one database*: a partition per month, say. Queries for March read only March; archiving January is a single quick command.
- **Sharding** splits the data across *many database servers*, each holding some of the customers, when one machine can't keep up at all.

Today you'll partition the paybill's payments in Postgres, and write the two ways of deciding which shard a customer lives on, and see why one of them makes adding a server painful.

## What you'll use

**Declarative partitioning** in Postgres:

```sql
CREATE TABLE payments (..., PRIMARY KEY (id, paid_on)) PARTITION BY RANGE (paid_on);
CREATE TABLE payments_2026_03 PARTITION OF payments FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE payments_default PARTITION OF payments DEFAULT;
```

- `FROM` is included and `TO` isn't, so months meet without overlapping.
- You insert into and query `payments`; Postgres puts each row in its partition and reads only the partitions a query can need. That's **partition pruning**, and you'll see it in `EXPLAIN`. It only works when the `WHERE` compares the partition key itself (`paid_on >= '2026-03-01'`), not a function of it (`date_trunc('month', paid_on) = ...`).
- A primary key or unique constraint must include the partition key, because each partition checks uniqueness on its own.
- `ALTER TABLE payments DETACH PARTITION payments_2026_01;` turns January into an ordinary table, in an instant: back it up, move it, or `DROP` it. `DROP TABLE` beats `DELETE` of a hundred million rows.
- `tableoid::regclass` tells you which partition a row came from.
- There's also `PARTITION BY LIST (county)` and `PARTITION BY HASH (id)`. MySQL has partitioning too, with different rules.

**Sharding** happens outside the database: your code (or a proxy) picks the server.

- **Modulo**: `shard = hash(key) % N`. Simple and even. But change `N` from 4 to 5 and about 80% of keys now belong somewhere else, so they all have to move.
- **Consistent hashing**: put the servers at points on a ring of hash values; a key belongs to the next server clockwise from its own hash. Add a server and it takes over only the keys just before its points: about `1/N` of them. Each server gets many points (**virtual nodes**) so the shares come out even. DynamoDB, Cassandra and many caches work this way.

Use a stable hash (here SHA-256). Python's `hash()` of a string changes every time Python starts.

## Steps

```bash
tools/psql.sh postgres -c "CREATE DATABASE big;"
tools/psql.sh big -f phase-8-expert/day-092-too-big-for-one-table/setup.sql
```

1. `starter/0-partitioned.sql`: the partitioned `payments` and its four partitions.
2. `starter/1-copy.sql` and `starter/2-partition_counts.sql`.
3. `starter/3-march_days.sql`: March's daily totals. Check `EXPLAIN` shows only the March partition.
4. `starter/4-archive_january.sql`.
5. `starter/shards.py`: `shard_for` and `moved_fraction`.
6. `pytest phase-8-expert/day-092-too-big-for-one-table`

## The kata: The Ring

In `starter/shards.py`, write the `Ring` class: add and remove nodes with their virtual points, and find a key's node. The tests add a fifth server and check that only about a fifth of the keys move, all of them to the new server.

## When you're stuck

- **`unique constraint on partitioned table must include all partitioning columns`**: the primary key has to be `(id, paid_on)`.
- **`no partition of relation "payments" found for row`**: there's no partition for that date. That's what `DEFAULT` is for.
- **March's plan scans every partition**: compare `paid_on` directly with dates. Wrapping it in a function or a cast hides it from pruning.
- **`partition` comes back as a number**: cast `tableoid::regclass`, then `::text`.
- **The ring moves keys between old nodes when you add one**: a key must go to the first point *greater than* its hash, wrapping round to the smallest point. Keep the points sorted and use `bisect_right`.
- **`remove` leaves points behind**: take off exactly the `replicas` points the node added: `h(f"{node}#{i}")`.
