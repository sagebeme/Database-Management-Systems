# Phase 5: Advanced MySQL

The MySQL that real applications lean on: constraints, window functions, recursive queries, triggers, stored procedures, indexes and JSON.

**You learn:** CHECK and ENUM, window functions, CTEs, recursive queries, triggers, stored procedures and functions, indexes, JSON.

**It ends with:** a school results system that keeps itself up to date.

## The days

| Day | Project | What it teaches |
|---|---|---|
| 53 | [Unique Users](day-053-unique-users/README.md) | constraints in depth: CHECK, ENUM, UNIQUE |
| 54 | [Fans by Country](day-054-fans-by-country/README.md) | ranking with window functions |
| 55 | [Running Totals](day-055-running-totals/README.md) | SUM OVER, LAG, LEAD, moving averages |
| 56 | [Who Reports to Whom](day-056-who-reports-to-whom/README.md) | CTEs and recursive CTEs |
| 57 | [Band Lifespans](day-057-band-lifespans/README.md) | date arithmetic |
| 58 | [Stock Goes Down](day-058-stock-goes-down/README.md) | triggers I |
| 59 | [Email Changed](day-059-email-changed/README.md) | triggers II: BEFORE UPDATE |
| 60 | [Add a Bonus](day-060-add-a-bonus/README.md) | stored procedures |
| 61 | [Average Scores](day-061-average-scores/README.md) | procedures, functions, cursors |
| 62 | [Finding Names Fast](day-062-finding-names-fast/README.md) | CREATE INDEX, prefix indexes, EXPLAIN |
| 63 | [Flexible Fields](day-063-flexible-fields/README.md) | JSON columns, generated columns |
| 64 | [Capstone: Results Day](day-064-capstone-results-day/README.md) | triggers, procedures, views and indexes together |

## How to test your work

**Run a day's tests:**

```bash
pytest phase-5-advanced-mysql/day-055-running-totals                       # every test for the day
pytest phase-5-advanced-mysql/day-055-running-totals -k kata               # only tests whose name contains "kata"
pytest phase-5-advanced-mysql/day-055-running-totals -x --tb=short         # stop at the first failure, with a short explanation
```

Each test runs one of your files and compares the result with the right answer. A failure shows what came back and what was expected, usually as rows like `('Nakuru', '12')`. From SQL files, every value comes back as text, and `NULL` as `'NULL'`. Read the first failure only, fix it, run again.

**Many tests change the data and run your file a second time**, so an answer typed in by hand, or one that only works for today's rows, fails the second run. If the first run passes and the second fails, your query depends on something it shouldn't (an id you typed, a row's position, a name spelled out).

**Run your work by hand:**

Load a day's data into a practice database, then run your file the way the tests do:

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS practice;"
tools/mysql.sh practice < phase-5-advanced-mysql/day-055-running-totals/setup.sql
tools/mysql.sh practice < phase-5-advanced-mysql/day-055-running-totals/starter/0-running_total.sql
```

`tools/mysql.sh practice` on its own opens a `mysql>` prompt in that database: the fastest place to try a query before saving it. If your query changed the data (an `INSERT`, `UPDATE` or `DELETE`), start clean: `tools/mysql.sh -e "DROP DATABASE practice; CREATE DATABASE practice;"` and load `setup.sql` again. The tests always start from a fresh database, so leftovers in yours never affect them.

**Triggers and procedures** need `DELIMITER` lines in the file, and they work through `tools/mysql.sh ... < file` exactly as they do in the tests. They don't work if you paste them into some GUI tools. To test a trigger, load your file, then run the statement that should fire it at the `mysql>` prompt and look at the table it should have changed.

**Still stuck?** Read the day's "When you're stuck" section first: it lists the mistakes people actually make. Then compare your output with the reference answer's. It spoils the answer, so it's the last resort:

```bash
diff <(tools/mysql.sh practice < phase-5-advanced-mysql/day-055-running-totals/starter/0-running_total.sql) <(tools/mysql.sh practice < phase-5-advanced-mysql/day-055-running-totals/solution/0-running_total.sql)
```

On Windows, run all of this in the Ubuntu (WSL) terminal, not PowerShell: see [WINDOWS.md](../WINDOWS.md).


## Further reading

- [MySQL: window functions](https://dev.mysql.com/doc/refman/8.4/en/window-functions.html), [triggers](https://dev.mysql.com/doc/refman/8.4/en/triggers.html) and [stored routines](https://dev.mysql.com/doc/refman/8.4/en/stored-routines.html).
- [Use The Index, Luke](https://use-the-index-luke.com/): how indexes really work, free online.
