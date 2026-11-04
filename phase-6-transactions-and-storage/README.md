# Phase 6: Transactions and storage

What happens when two people change the same row at once, how a database survives a power cut, and how it finds one row among millions. Half of this phase is GATE theory, half is building the machinery in Python.

**You learn:** ACID, isolation levels, schedules, recoverability, conflict and view serializability, locking, timestamps, deadlocks, recovery, file organisation, B-trees and B+ trees, index design.

**It ends with:** a tiny storage engine with a B+ tree index and a log.

## The days

| Day | Project | What it teaches |
|---|---|---|
| 65 | [Send Money](day-065-send-money/README.md) | transactions, COMMIT, ROLLBACK, ACID |
| 66 | [Two Tellers, One Account](day-066-two-tellers-one-account/README.md) | lost updates, dirty and non-repeatable reads, phantoms |
| 67 | [Isolation Levels](day-067-isolation-levels/README.md) | what each level allows, in MySQL and PostgreSQL |
| 68 | [Can We Undo It?](day-068-can-we-undo-it/README.md) | schedules, recoverable, cascadeless and strict |
| 69 | [As If One at a Time](day-069-as-if-one-at-a-time/README.md) | conflict serializability, precedence graphs |
| 70 | [View Serializability](day-070-view-serializability/README.md) | view equivalence, blind writes |
| 71 | [Locks](day-071-locks/README.md) | two-phase locking, SELECT ... FOR UPDATE, deadlocks |
| 72 | [Who Came First](day-072-who-came-first/README.md) | timestamp ordering, Thomas write rule, wait-die and wound-wait |
| 73 | [After the Blackout](day-073-after-the-blackout/README.md) | write-ahead logging, undo, redo, checkpoints |
| 74 | [How Many Pages](day-074-how-many-pages/README.md) | file organisation, blocking factor, index sizes |
| 75 | [B-Trees](day-075-b-trees/README.md) | search and insert in a B-tree |
| 76 | [B+ Trees](day-076-b-plus-trees/README.md) | order, insert, split, range scans |
| 77 | [Where the Rows Live](day-077-where-the-rows-live/README.md) | clustered and secondary indexes, composite and covering indexes |
| 78 | [Capstone: The SACCO Engine](day-078-capstone-the-sacco-engine/README.md) | a heap file, a B+ tree index and a log, in Python |

## Outside the hundred days

These don't count towards the hundred days, and nothing later depends on them. They're there to make the theory stick.

- [worked-examples.md](worked-examples.md): nine problems (recoverability, precedence graphs, view serializability, 2PL, timestamps, wait-die, recovery, block counts, B+ trees) solved step by step.
- [Checkpoint 3: Practice Test 3](checkpoint-3-practice-test-3/README.md): a 27-mark paper on this phase. Take it after Day 78.

## How to test your work

**Run a day's tests:**

```bash
pytest phase-6-transactions-and-storage/day-069-as-if-one-at-a-time                       # every test for the day
pytest phase-6-transactions-and-storage/day-069-as-if-one-at-a-time -k kata               # only tests whose name contains "kata"
pytest phase-6-transactions-and-storage/day-069-as-if-one-at-a-time -x --tb=short         # stop at the first failure, with a short explanation
```

Each test runs one of your files and compares the result with the right answer. A failure shows what came back and what was expected, usually as rows like `('Nakuru', '12')`. From SQL files, every value comes back as text, and `NULL` as `'NULL'`. Read the first failure only, fix it, run again.

**Many tests change the data and run your file a second time**, so an answer typed in by hand, or one that only works for today's rows, fails the second run. If the first run passes and the second fails, your query depends on something it shouldn't (an id you typed, a row's position, a name spelled out).

**Run your work by hand:**

- **Schedules** are written as text: `"r1(A) w2(A) c1"`. Try your functions at a Python prompt: `PYTHONPATH=tools python -i phase-6-transactions-and-storage/day-069-as-if-one-at-a-time/starter/serial.py`, then `from coursekit.schedules import parse` and pass your functions `parse("r1(A) w2(A) c1")`.
- **Two-session days** (Days 65 to 67, 71) need two terminals, each with its own `tools/mysql.sh practice` (or `tools/psql.sh practice` from Day 67), so you can watch one transaction wait for the other. The tests do the same thing with two connections.
- **PostgreSQL arrives on Day 67**: `tools/psql.sh postgres -c "CREATE DATABASE practice;"`, then `tools/psql.sh practice -f path/to/file.sql`. Inside `psql`, `\dt` lists tables and `\q` quits.
- **`answers.py`**: replace each `None`.

**Still stuck?** Read the day's "When you're stuck" section first: it lists the mistakes people actually make. Then open the same file in `solution/` and compare. It spoils the answer, so read it, close it, and write your own version from memory.

On Windows, run all of this in the Ubuntu (WSL) terminal, not PowerShell: see [WINDOWS.md](../WINDOWS.md).


## Further reading

- [CMU 15-445 Database Systems](https://15445.courses.cs.cmu.edu/): free lectures on storage, indexes, concurrency and recovery.
- *Database System Concepts* ([db-book.com](https://db-book.com/)), chapters 13 to 19.
- [MySQL: InnoDB locking](https://dev.mysql.com/doc/refman/8.4/en/innodb-locking.html).
