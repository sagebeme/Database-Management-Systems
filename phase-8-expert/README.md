# Phase 8: Expert

Running databases for real: reading query plans, partitioning and sharding, backups, security (including storing passwords safely), warehousing, then three portfolio projects, the final exam and your own production database.

**You learn:** query plans and join algorithms, partitioning and sharding, replication and backups, security and password hashing, data warehousing.

**It ends with:** a production-ready database for a real business, designed and defended.

## The days

| Day | Project | What it teaches |
|---|---|---|
| 91 | [Reading Query Plans](day-091-reading-query-plans/README.md) | EXPLAIN ANALYZE, join algorithms, cost |
| 92 | [Too Big for One Table](day-092-too-big-for-one-table/README.md) | partitioning and sharding |
| 93 | [Never Lose Data](day-093-never-lose-data/README.md) | backups, restores, replication |
| 94 | [Lock It Down](day-094-lock-it-down/README.md) | least privilege, row-level security, auditing, password hashing |
| 95 | [The Data Warehouse](day-095-the-data-warehouse/README.md) | star schemas, OLTP vs OLAP, ETL |
| 96 | [Portfolio: SACCO Database](day-096-portfolio-sacco-database/README.md) | a brief and its tests, no walkthrough |
| 97 | [Portfolio: The SQL Interview](day-097-portfolio-the-sql-interview/README.md) | twenty hard questions, HackerRank-style |
| 98 | [Portfolio: Build a Key-Value Store](day-098-portfolio-build-a-key-value-store/README.md) | a log-structured store with compaction |
| 99 | [The Final Exam](day-099-the-final-exam/README.md) | a full GATE-style subject test |
| 100 | [Capstone: Your Own Production Database](day-100-capstone-your-own-production-database/README.md) | design doc, migrations, constraints, indexes, roles and an undo |

## How to test your work

**Run a day's tests:**

```bash
pytest phase-8-expert/day-091-reading-query-plans                       # every test for the day
pytest phase-8-expert/day-091-reading-query-plans -k kata               # only tests whose name contains "kata"
pytest phase-8-expert/day-091-reading-query-plans -x --tb=short         # stop at the first failure, with a short explanation
```

Each test runs one of your files and compares the result with the right answer. A failure shows what came back and what was expected, usually as rows like `('Nakuru', '12')`. From SQL files, every value comes back as text, and `NULL` as `'NULL'`. Read the first failure only, fix it, run again.

**Many tests change the data and run your file a second time**, so an answer typed in by hand, or one that only works for today's rows, fails the second run. If the first run passes and the second fails, your query depends on something it shouldn't (an id you typed, a row's position, a name spelled out).

**Run your work by hand:**

Everything here is PostgreSQL and Python:

```bash
tools/psql.sh postgres -c "CREATE DATABASE practice;"
tools/psql.sh practice -f phase-8-expert/day-091-reading-query-plans/setup.sql
tools/psql.sh practice -f phase-8-expert/day-091-reading-query-plans/starter/1-explain.sql
```

- **Query plans**: put `EXPLAIN ANALYZE` in front of any query at the `psql` prompt to see what PostgreSQL actually did.
- **Backups (Day 93)** use `pg_dump` and `pg_restore`, which must be version 17 like the server: `pg_dump --version`.
- **Roles (Days 94 and 100)** belong to the whole server, not one database. If a role is left over from an earlier try: `tools/psql.sh postgres -c "DROP ROLE name;"` after dropping the databases that use it.
- **Portfolio days (96 to 98)** have no walkthrough: the tests are the client's acceptance checks. Run them often.

**Still stuck?** Read the day's "When you're stuck" section first: it lists the mistakes people actually make. Then open the same file in `solution/` and compare. It spoils the answer, so read it, close it, and write your own version from memory.

On Windows, run all of this in the Ubuntu (WSL) terminal, not PowerShell: see [WINDOWS.md](../WINDOWS.md).


## Further reading

- [PostgreSQL: using EXPLAIN](https://www.postgresql.org/docs/17/using-explain.html).
- [Use The Index, Luke](https://use-the-index-luke.com/).
- *Designing Data-Intensive Applications* by Martin Kleppmann: replication, partitioning and storage engines, the background for this whole phase.
