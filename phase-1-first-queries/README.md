# Phase 1: SQL from zero

Your first tables and your first queries. Every day is one small job for someone (a duka owner, a matatu SACCO, a county office), done with MySQL.

**You learn:** databases and tables, data types, inserting, selecting, filtering, sorting, aggregates, grouping, NULL, functions, character sets.

**It ends with:** a weather report for Kenya's counties.

## The days

| Day | Project | What it teaches |
|---|---|---|
| 1 | [Hello, MySQL](day-001-hello-mysql/README.md) | the server, SHOW, CREATE and DROP DATABASE, idempotent scripts |
| 2 | [The Chama Register](day-002-chama-register/README.md) | CREATE TABLE, data types, SHOW TABLES, DESCRIBE |
| 3 | [Sukuma Prices](day-003-sukuma-prices/README.md) | INSERT, SELECT, SHOW CREATE TABLE |
| 4 | [Matatu Stages](day-004-matatu-stages/README.md) | WHERE, comparison operators, IS NULL |
| 5 | [M-Pesa Search](day-005-mpesa-search/README.md) | AND, OR, NOT, IN, BETWEEN, LIKE |
| 6 | [KCSE Top Ten](day-006-kcse-top-ten/README.md) | ORDER BY, LIMIT, OFFSET, DISTINCT |
| 7 | [Fixing the Register](day-007-fixing-the-register/README.md) | UPDATE and DELETE, safely |
| 8 | [Shop Totals](day-008-shop-totals/README.md) | COUNT, SUM, AVG, MIN, MAX |
| 9 | [Sales by Category](day-009-sales-by-category/README.md) | GROUP BY |
| 10 | [Best-Selling Saccos](day-010-best-selling-saccos/README.md) | HAVING, and the order SQL runs a query in |
| 11 | [Missing Phone Numbers](day-011-missing-phone-numbers/README.md) | NULL, three-valued logic, COALESCE |
| 12 | [Receipts and Due Dates](day-012-receipts-and-due-dates/README.md) | string, number and date functions, CASE |
| 13 | [Majina na Emoji](day-013-majina-na-emoji/README.md) | character sets, utf8mb4, collations |
| 14 | [Capstone: County Weather Report](day-014-county-weather-report/README.md) | everything in Phase 1 on one dataset |

## How to test your work

**Run a day's tests:**

```bash
pytest phase-1-first-queries/day-004-matatu-stages                       # every test for the day
pytest phase-1-first-queries/day-004-matatu-stages -k kata               # only tests whose name contains "kata"
pytest phase-1-first-queries/day-004-matatu-stages -x --tb=short         # stop at the first failure, with a short explanation
```

Each test runs one of your files and compares the result with the right answer. A failure shows what came back and what was expected, usually as rows like `('Nakuru', '12')`. From SQL files, every value comes back as text, and `NULL` as `'NULL'`. Read the first failure only, fix it, run again.

**Many tests change the data and run your file a second time**, so an answer typed in by hand, or one that only works for today's rows, fails the second run. If the first run passes and the second fails, your query depends on something it shouldn't (an id you typed, a row's position, a name spelled out).

**Run your work by hand:**

Load a day's data into a practice database, then run your file the way the tests do:

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS practice;"
tools/mysql.sh practice < phase-1-first-queries/day-004-matatu-stages/setup.sql
tools/mysql.sh practice < phase-1-first-queries/day-004-matatu-stages/starter/0-cheap_routes.sql
```

`tools/mysql.sh practice` on its own opens a `mysql>` prompt in that database: the fastest place to try a query before saving it. If your query changed the data (an `INSERT`, `UPDATE` or `DELETE`), start clean: `tools/mysql.sh -e "DROP DATABASE practice; CREATE DATABASE practice;"` and load `setup.sql` again. The tests always start from a fresh database, so leftovers in yours never affect them.

**Still stuck?** Read the day's "When you're stuck" section first: it lists the mistakes people actually make. Then compare your output with the reference answer's. It spoils the answer, so it's the last resort:

```bash
diff <(tools/mysql.sh practice < phase-1-first-queries/day-004-matatu-stages/starter/0-cheap_routes.sql) <(tools/mysql.sh practice < phase-1-first-queries/day-004-matatu-stages/solution/0-cheap_routes.sql)
```

On Windows, run all of this in the Ubuntu (WSL) terminal, not PowerShell: see [WINDOWS.md](../WINDOWS.md).


## Further reading

- [SQLBolt](https://sqlbolt.com/): short interactive lessons, good for a second explanation of a topic.
- [MySQL 8.4 Reference Manual](https://dev.mysql.com/doc/refman/8.4/en/): look up any function or statement you meet.
- [HackerRank SQL](https://www.hackerrank.com/domains/sql): the Basic Select and Aggregation sections match this phase.
