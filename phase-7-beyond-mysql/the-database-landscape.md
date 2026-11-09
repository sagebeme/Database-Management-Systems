# The database landscape

A map, not a lesson. By Day 90 you've used four databases. Job adverts and system designs will name dozens more. This page sorts them into families, says what each family is for, and points back to the day where you met the idea. Read it after Day 90, and again whenever someone says "we should use X".

Nothing here has tests, and nothing later depends on it.

---

## The rule that settles most arguments

**Start with PostgreSQL (or the MySQL you already run). Add something else only when you can name the problem it solves.**

A relational database with good indexes copes with far more than most people expect: millions of rows on one ordinary server, with JSON (Day 80), full-text search (Day 80) and transactions you can trust (Phase 6). Each extra database you add is another thing to back up, secure, monitor and keep in sync. "Netflix uses it" isn't a problem you have.

---

## 1. Relational databases: tables, SQL, transactions

The family this whole course is about.

| Database | Where you'll meet it |
|---|---|
| **PostgreSQL** | The default for new projects. Strict, full of features, free. Days 67 and 79–80. |
| **MySQL / MariaDB** | Huge numbers of websites and older systems. MariaDB is a fork of MySQL by its original authors. Phases 1–5. |
| **SQLite** | A whole database in one file, with no server. It's inside every phone, most browsers, and countless apps. It's the right choice for a single app on one device, for tests, and for small sites. |
| **Microsoft SQL Server** | Banks, governments and companies that run on Microsoft. Its SQL dialect is called T-SQL. |
| **Oracle Database** | Big, old, expensive, and still running many banks, telcos and governments. Its dialect is called PL/SQL. |

Your SQL transfers: `SELECT`, joins, `GROUP BY` and window functions read the same everywhere. What changes is the small stuff, such as `LIMIT 10` vs `TOP 10` vs `FETCH FIRST 10 ROWS ONLY`, auto-increment keys, and date functions.

**Hosted for you:** Amazon RDS and Aurora, Google Cloud SQL, Azure, Supabase and Neon run Postgres or MySQL for you. Backups (Day 93), patching and replicas are then their job, and you pay for that.

---

## 2. When one server isn't enough

Two ways to grow:

- **Scale up (vertical):** a bigger machine, with more memory, faster disks and more CPUs. It's simple and needs no code changes. It's the first thing to try, and it goes further than people think. It stops at the biggest machine you can buy, and it's still one machine that can fail.
- **Scale out (horizontal):** more machines.
  - **Read replicas** copy every change to other servers, which answer reads (Day 93).
  - **Sharding** splits the rows across servers (Day 92). It's powerful, but joins and transactions across shards get hard, and your code has to know where everything lives.

**The CAP theorem.** When the network between your servers breaks, and it will, a distributed database has to choose:

- It can stay **consistent**: refuse requests until the servers agree.
- It can stay **available**: answer anyway, possibly with stale data.

It can't do both during the break. Banks lean towards consistent; a social feed leans towards available.

**Distributed SQL (sometimes called NewSQL).** CockroachDB, YugabyteDB, TiDB and Google Spanner shard and replicate for you, but keep SQL and real transactions. They feel like Postgres or MySQL, and some speak their protocols. The price is that every write needs several servers to agree, which makes it slower, and the system is more complicated to run. Reach for one when you truly need many regions, or more writes than one server can take.

---

## 3. NoSQL: other shapes of data

"NoSQL" just means "not a relational table". It covers very different things.

| Family | Examples | Good for | You met it |
|---|---|---|---|
| **Document** | MongoDB, Firestore, CouchDB | records that are naturally a nested whole and read together, like a product with its variants | Days 83–86 |
| **Key-value** | Redis, Valkey, DynamoDB, Memcached | looking things up by key, very fast: caches, sessions, counters, rate limits | Days 87–89 |
| **Wide-column** | Cassandra, ScyllaDB | enormous write volumes spread over many machines, such as sensor readings or messages | |
| **Graph** | Neo4j, Amazon Neptune | data that is mostly *relationships*, such as who knows whom or fraud rings, where you'd otherwise write joins many levels deep | Day 56's recursive CTEs do small versions of this |

The trade is usually the same: a simpler, faster path for one shape of data, in exchange for fewer guarantees, fewer kinds of query, or more work in your code. Day 86 (embed or reference) is the whole decision in miniature.

---

## 4. Search engines

**Elasticsearch / OpenSearch**, **Meilisearch** and **Typesense** are built for search boxes: typo tolerance ("mtatu" finds "matatu"), ranking by relevance, filters with counts beside them ("Nairobi (120)"), and search as you type.

They aren't the source of truth. You copy data into them from your real database and accept that the copy is a little behind. Postgres full-text search (Day 80) handles plenty of sites on its own. Add a search engine when search *is* the product, or Postgres's ranking isn't good enough.

---

## 5. Analytics: warehouses and column stores

Your app's database is built for **OLTP**: many small reads and writes, one row at a time. Questions like "total sales by county by month for three years" are **OLAP**: they read a few columns from millions of rows. Day 95 covered the difference and the star schema.

- **Column stores** keep each column together on disk, so a query reads only the columns it needs. They also compress well.
  - **ClickHouse** is fast and open source.
  - **DuckDB** is like SQLite for analytics: it runs inside your program and reads CSV and Parquet files directly. It's brilliant on a laptop.
- **Cloud warehouses** (BigQuery, Snowflake, Amazon Redshift) store and query terabytes, and charge by what you scan or how much computing you use.

**Big data, briefly.** Hadoop (and Hive on top of it) spread files and batch jobs over many cheap machines. Spark made that much faster. Today most companies use a cloud warehouse, or files in cloud storage queried with SQL (a "lakehouse"), instead of running Hadoop themselves. When a job advert says "big data", it usually means Spark and a warehouse.

---

## 6. Moving data around: streams

**Kafka** (and Redpanda, or the cloud versions) isn't a database you query. It's a log: an append-only list of events ("payment received", "ticket scanned") that many programs can read at their own pace. The idea is the same as the write-ahead log from Day 73, made into a product.

Teams use it to feed the warehouse, the search engine and the cache from one stream of changes, often captured straight from the database's own log (called "change data capture", or CDC). You'll meet it in data-engineering jobs, rarely in a first backend job.

---

## 7. Special shapes

- **Time series:** TimescaleDB (a Postgres extension) or InfluxDB, for readings over time, such as meters, prices or server metrics. They make "average per five minutes over the last week" fast, and drop old data automatically.
- **Vectors:** pgvector (a Postgres extension), Pinecone, Qdrant. They store each document as a list of numbers produced by an AI model, and find the *most similar* ones. That's how "search by meaning" and many AI assistants find the right documents. Try pgvector before a separate product.
- **Geography:** PostGIS (a Postgres extension). "Every matatu stage within 500 m of here" is one query.

Notice how many of these are Postgres extensions. That's a big part of why it's the default.

---

## Choosing, in one table

| You need | Start with |
|---|---|
| An app's data, money, anything that must be right | PostgreSQL or MySQL |
| One app on one device, or tests | SQLite |
| Pages or results that are slow and read often | Redis in front of your database (Day 89) |
| Nested records always read whole | Postgres JSONB first (Day 80), then MongoDB |
| A real search box | Postgres full-text first, then Meilisearch, Typesense or Elasticsearch |
| Reports over years of data | A separate warehouse or DuckDB, fed from the app's database (Day 95) |
| Writes from many regions, more than one server can take | Distributed SQL (CockroachDB, Spanner) or Cassandra |
| AI "search by meaning" | pgvector |

## Check yourself

1. A startup with 2,000 users wants MongoDB "because it scales". What would you ask them first?
2. What's the difference between adding a read replica and sharding? Which one helps when *writes* are the problem?
3. Why is a search engine's copy of your data allowed to be a few seconds behind, but your payments table isn't?
4. A report query on the app's database takes 40 seconds and slows the checkout down. Name two fixes from this page.

<details>
<summary>Answers</summary>

1. What problem they have today that Postgres or MySQL can't handle. 2,000 users fit comfortably on one small server. Then ask whether their data is really nested documents, or related records that need joins and transactions.
2. A replica copies *all* the data to another server to share the **reads**. Every write still goes to the one main server. Sharding splits the data so each server holds *some* rows, which spreads the **writes**. When writes are the problem, sharding (or distributed SQL) helps; replicas don't.
3. Search results that are a moment stale cost nothing: the product appears a second later. Payments must never be lost, doubled or misread, so they stay in the database with transactions (Phase 6), and the search engine only gets a copy.
4. Run reports on a read replica, so they don't compete with checkout. Or copy the data to a warehouse or DuckDB in a reporting shape (a star schema, Day 95). Adding the right index (Day 91) may also be enough.

</details>
