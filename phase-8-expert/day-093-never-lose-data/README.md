# Day 93: Never Lose Data

## The brief

Every year some Kenyan business loses its records to a dead disk, a ransomware attack, a fire, or an intern running `DELETE` without a `WHERE`. The ones that survive had a **backup they had actually restored** and checked. A backup nobody has restored isn't a backup; it's a hope.

Today you'll back up a SACCO's database, restore it somewhere safe, prove the copy is identical, and work out which backups to keep. You'll also learn the two numbers every backup plan is judged by, and why a replica is not a backup.

## What you'll use

**Logical backups** with Postgres's tools:

```bash
pg_dump -Fc -f sacco.dump sacco          # the whole database, in the compressed "custom" format
createdb sacco_restored                   # a NEW database: never restore over live data
pg_restore --no-owner -d sacco_restored sacco.dump
```

`pg_dump` takes a consistent snapshot without stopping the app (Day 67's MVCC at work). MySQL's equivalent is `mysqldump --single-transaction`. Use the tools from the same major version as the server, or newer.

**Proving a restore**: compare every table's row count and a checksum of its contents.

```sql
SELECT count(*), md5(string_agg(t::text, ',' ORDER BY id)) FROM members AS t;
```

`t::text` turns a whole row into text, like `(1,"Member 1",254700007919)`.

**Two numbers** every plan is judged by:

- **RPO**, recovery point objective: how much data you can afford to lose, measured in time. Nightly backups mean an RPO of up to 24 hours.
- **RTO**, recovery time objective: how long you can afford to be down while you recover.

**Getting the RPO down**:

- **WAL archiving** (Day 73's log, kept): copy every finished WAL file somewhere safe. Restore the last base backup (`pg_basebackup`), then replay the WAL up to any moment you choose: **point-in-time recovery**, "put it back to 14:31, just before the bad `DELETE`".
- **Replication**: a standby server applies the primary's WAL as it arrives, ready to take over in seconds. *Synchronous* replication waits for the standby before saying "committed", so nothing committed is lost; *asynchronous* doesn't wait, so the last moments can be lost in a failover.

**A replica is not a backup.** It copies mistakes faithfully and instantly: `DROP TABLE` on the primary is a dropped table on the replica a millisecond later.

**The 3-2-1 rule**: 3 copies of your data, on 2 different kinds of storage, 1 of them somewhere else (another building, another cloud account).

**Retention**: keeping every nightly backup forever is expensive; keeping only last night's is reckless. **Grandfather-father-son** keeps the last week's dailies, the last month's weeklies and the last year's monthlies.

## Steps

```bash
tools/psql.sh postgres -c "CREATE DATABASE sacco;"
tools/psql.sh sacco -f phase-8-expert/day-093-never-lose-data/setup.sql
```

Try `pg_dump` and `pg_restore` by hand (use the version 17 tools: `/usr/lib/postgresql/17/bin/pg_dump` on Ubuntu if an older one comes first on your `PATH`). Then:

1. `starter/backup.py`: `tool`, `conn_args` and `run` are done. Write `dump`, `restore`, `fingerprint` and `differences`.
2. `starter/answers.py`.
3. `pytest phase-8-expert/day-093-never-lose-data`

## The kata: What to Keep

In `starter/backup.py`, write `keep(backups, today)`: given the dates with a nightly backup, return the ones grandfather-father-son keeps.

## When you're stuck

- **`pg_dump: error: aborting because of server version mismatch`**: an older `pg_dump` came first. Use `tool("pg_dump")`, which finds the newest installed.
- **`restore` says `database ... already exists`**: good, that's what should happen. Let the `RuntimeError` through.
- **The restored database is empty**: the dump file is the last argument to `pg_restore`, and `-d` names the database to restore *into*.
- **`role "..." does not exist`** during restore: add `--no-owner`, so the objects belong to whoever restores them.
- **`fingerprint` is the same after an edit**: aggregate in a fixed order (`ORDER BY id` inside `string_agg`), and over whole rows (`t::text`), not one column.
- **The kata keeps too many**: a backup kept for two reasons (a Sunday that's also in the last week) is still one backup. Return a set.
