# Day 73: After the Blackout

## The brief

KPLC cuts the power at 7:42 pm. The SACCO's database server goes down mid-afternoon rush: one transfer had committed, two were half-way through. When it boots, the members' balances must show every committed transaction in full and nothing at all of the others. That's the **A** and **D** of ACID, and it's the job of the **log**.

Memory is fast and forgets everything in a blackout; disk is slow and remembers. A database changes pages in memory (the *buffer pool*) and writes them to disk later, whenever it suits it. So after a crash the disk can hold changes from transactions that never committed, and be missing changes from ones that did. Today you'll write the recovery that fixes both, from the log alone.

## What you'll use

**The log** is an append-only file of records, written to disk *before* the data it describes. That's **write-ahead logging (WAL)**:

```
("start", 1)
("update", 1, "A", 100, 80)     T1 changed A from 100 to 80
("commit", 1)
```

Three ways to use it, depending on what the log records and when pages may hit the disk:

| | Log keeps | Page with T's change may reach disk | Recovery |
|---|---|---|---|
| **Undo** | old values | any time, but T's commit record only after all its pages | backwards: put the old value back for every update by a transaction with no commit |
| **Redo** | new values | only after T's commit record is on disk | forwards: write the new value for every update by a committed transaction |
| **Undo/redo** | both | any time, as long as the log record is on disk first | redo committed transactions forwards, then undo the rest backwards |

Undo forces lots of page writes at commit; redo has to keep every uncommitted change in memory. Undo/redo frees the buffer pool to write whenever it likes, which is why InnoDB, Postgres and nearly everyone use it (with refinements, in an algorithm called ARIES).

**Losers** are transactions with a start record but no commit or abort: the crash caught them. An abort record means the transaction had already been rolled back before the crash.

**Recovery must be safe to run twice**, because the power can go again during recovery. Setting a value ("A is 80") is safe to repeat; adding to it ("A goes down by 20") isn't. That's why the log stores values.

**Checkpoints**: without them, recovery reads the whole log back to the day the database was installed. A checkpoint writes every dirty page to disk and logs `("checkpoint", (2, 5))`, the transactions still running at that moment. Recovery can then start at the checkpoint, except that it must go further back to the start of any listed transaction that never finished, to undo its early changes.

**In InnoDB**: the *redo log* (`#innodb_redo/` files) is the WAL; old row versions live in *undo logs*, which also serve MVCC reads (Day 67). `innodb_flush_log_at_trx_commit = 1` flushes the redo log at every commit, so a committed transaction survives a crash. Set it to 2 or 0 and commits are faster, but a crash can lose the last second of them. That trade-off is a real decision teams make.

## Steps

Pure Python, plus one look at MySQL:

```bash
tools/mysql.sh -e "SHOW VARIABLES LIKE 'innodb_flush%'; SHOW VARIABLES LIKE 'innodb_redo%';"
```

1. Work the test file's `LOG` by hand first: after the crash, which transactions are losers, and what must A, B and C end up as?
2. `starter/recovery_log.py`: `losers`, `undo_recover`, `redo_recover`, `undo_redo_recover`, `scan_from`.
3. `starter/answers.py`.
4. `pytest phase-6-transactions-and-storage/day-073-after-the-blackout`

## The kata: Write-Ahead or Not

In `starter/recovery_log.py`, write `follows_wal(events)`. Follow a log buffer in memory and the log on disk, and return the index of the first event that breaks a rule: a page written while one of its updates is still only in the buffer, or a customer told "it's done" before the commit record is on disk. `None` if every event is fine.

## When you're stuck

- **Undo gives the wrong value when one transaction changed an item twice**: go *backwards*, so the oldest old value is written last.
- **Redo gives T2's value when T3 changed it later and committed**: go *forwards*, so the newest committed value is written last.
- **"don't change the dict you were given"**: start with `disk = dict(disk)`.
- **The aborted transaction gets undone again**: an abort record means it's finished. Only start-without-commit-or-abort counts as a loser.
- **`scan_from` returns the checkpoint when a listed transaction never finished**: you need its start record, which is earlier.
- **"MySQL doesn't know that setting"**: the answer is the variable name as a string, without `@@`.
