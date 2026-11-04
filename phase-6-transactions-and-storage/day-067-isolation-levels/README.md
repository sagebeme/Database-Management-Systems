# Day 67: Isolation Levels

## The brief

Yesterday's anomalies have a standard cure: run every transaction as if it were alone. That's **serializable**, and it costs waiting, because transactions queue behind each other's locks or get refused and retried. So SQL offers **isolation levels**: weaker promises that run faster, each allowing some anomalies. Every database picks a default, and they don't pick the same one.

Today you don't take the textbook's word for it. You write three experiments, each one two connections racing on purpose, and run them at all four levels on **MySQL and PostgreSQL**. The tests check that your experiments find what really happens.

## What you'll use

**The standard's table**, what each level *allows* (an engine may do better):

| Level | Dirty read | Non-repeatable read | Phantom |
|---|---|---|---|
| `READ UNCOMMITTED` | allowed | allowed | allowed |
| `READ COMMITTED` | — | allowed | allowed |
| `REPEATABLE READ` | — | — | allowed |
| `SERIALIZABLE` | — | — | — |

**Setting the level** for the next transaction:

```sql
-- MySQL                                              -- PostgreSQL
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;       BEGIN ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
```

(`levels.py`'s `begin()` does this for you.) Check the current one with `SELECT @@transaction_isolation;` in MySQL, or `SHOW transaction_isolation;` in PostgreSQL.

**How the engines really do it:**

- **Snapshots (MVCC).** Both engines keep old versions of changed rows. A reader at `REPEATABLE READ` sees the database as it was when its transaction first read, so other people's later commits are invisible to it, phantoms included. At `READ COMMITTED`, every statement takes a fresh snapshot.
- **PostgreSQL never shows dirty reads**: its `READ UNCOMMITTED` behaves like `READ COMMITTED`.
- **MySQL's `SERIALIZABLE` uses locks**: every plain `SELECT` becomes a locking read, so a writer waits for the reader to finish. **PostgreSQL's** uses SSI (serializable snapshot isolation): nobody waits, but at commit one transaction may be refused with `could not serialize access`, and the app must retry it.
- **Write skew** (the kata) is the anomaly snapshots don't stop. Two transactions read the same facts, each changes a *different* row, and together they break a rule neither broke alone. Only `SERIALIZABLE` (or an explicit lock) stops it.
- **Defaults**: MySQL (InnoDB) uses `REPEATABLE READ`; PostgreSQL uses `READ COMMITTED`.

**Writing the experiments**: two connections in one thread is enough. Connection A does something and *doesn't* commit; B looks; then A commits or rolls back. If B (or A) has to wait for a lock, it would wait forever in one thread, so `short_waits()` makes it give up after a second, and `blocked()` turns that into `True`. End every transaction with `cur.execute("COMMIT")` or `cur.execute("ROLLBACK")`.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS levels;"
tools/mysql.sh levels < phase-6-transactions-and-storage/day-067-isolation-levels/setup.sql
psql -h 127.0.0.1 -p 5434 -U postgres -c "CREATE DATABASE levels;"
psql -h 127.0.0.1 -p 5434 -U postgres -d levels -f phase-6-transactions-and-storage/day-067-isolation-levels/setup.sql
```

Try it by hand first: two terminals, one `tools/mysql.sh levels` each. In the first, `SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED; START TRANSACTION; SELECT balance FROM accounts;`. In the second, `START TRANSACTION; UPDATE accounts SET balance = 9999;`. Back in the first, `SELECT balance FROM accounts;` again.

1. `starter/levels.py`: `sees_uncommitted`, `repeatable`, `sees_phantom`.
2. `starter/answers.py`: the standard's table, the defaults, and what you found.
3. `pytest phase-6-transactions-and-storage/day-067-isolation-levels`

## The kata: Write Skew

In `starter/kata.py`, write `write_skew(connect, engine, level)`. Dr Achieng and Dr Barasa are both on call, and the rule is that at least one must stay. Each checks ("2 on call, so I can go"), each takes *themselves* off, and each commits. Return how many are left on call. Below `SERIALIZABLE`, both engines end with 0.

## When you're stuck

- **Everything waits for 50 seconds**: call `short_waits()` on the connection that might wait, before it waits.
- **`Lock wait timeout exceeded` escapes from your function**: wrap the statement that might wait in `blocked(lambda: ...)`.
- **PostgreSQL says `current transaction is aborted, commands ignored until end of transaction block`**: after any error in PostgreSQL, the transaction must be rolled back before that connection can do anything else.
- **`repeatable` is `True` at `READ COMMITTED`**: B must stay in one transaction for both reads. Don't commit between them, and make sure `begin()` ran before the first read.
- **The phantom never appears**: A has to *commit* its insert before B's second count.
- **The kata ends with 2 on call at `READ COMMITTED`**: each doctor should update only their own row (`WHERE name = ...`). Updating both rows makes it an ordinary write conflict, which locks catch.
