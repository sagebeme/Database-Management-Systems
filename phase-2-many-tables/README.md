# Phase 2: Many tables

Real data never fits in one table. This phase connects tables with keys, then asks questions across them with subqueries and every kind of join.

**You learn:** keys and constraints, foreign keys, subqueries, joins of every kind, many-to-many, changing tables, users and privileges, views, importing data.

**It ends with:** a report on Riverwood, a Kenyan film and TV database.

## The days

| Day | Project | What it teaches |
|---|---|---|
| 15 | [One Table Is Not Enough](day-015-one-table-is-not-enough/README.md) | repeated data and the trouble it causes |
| 16 | [Rules for Rows](day-016-rules-for-rows/README.md) | PRIMARY KEY, AUTO_INCREMENT, UNIQUE, NOT NULL, DEFAULT |
| 17 | [Counties and Towns](day-017-counties-and-towns/README.md) | FOREIGN KEY, ON DELETE |
| 18 | [Towns in Nakuru](day-018-towns-in-nakuru/README.md) | subqueries |
| 19 | [Town, County](day-019-town-county/README.md) | INNER JOIN |
| 20 | [Every Town, Even Alone](day-020-every-town-even-alone/README.md) | LEFT, RIGHT and full outer joins |
| 21 | [Riverwood: Shows and Genres](day-021-shows-and-genres/README.md) | many-to-many and junction tables |
| 22 | [Not a Comedy](day-022-not-a-comedy/README.md) | anti-joins, NOT IN, NOT EXISTS |
| 23 | [Ratings](day-023-ratings/README.md) | joins with aggregates |
| 24 | [Changing the Shape](day-024-changing-the-shape/README.md) | ALTER TABLE, DROP, TRUNCATE vs DELETE |
| 25 | [Who Can See What](day-025-who-can-see-what/README.md) | users, GRANT, REVOKE |
| 26 | [Views](day-026-views/README.md) | CREATE VIEW, updatable views |
| 27 | [Loading Real Data](day-027-loading-real-data/README.md) | importing CSV, LOAD DATA |
| 28 | [Capstone: The Riverwood Report](day-028-capstone-the-riverwood-report/README.md) | twelve questions about a TV database |

## Outside the hundred days

These don't count towards the hundred days, and nothing later depends on them. They're there to make the theory stick.

- [Extra: Predict the Output](extra-predict-the-output/README.md): seventeen "what does this query return?" questions on the traps exams love (`NULL`, empty subqueries, `ALL` and `ANY`, outer joins). Do it after Day 28.

## How to test your work

**Run a day's tests:**

```bash
pytest phase-2-many-tables/day-019-town-county                       # every test for the day
pytest phase-2-many-tables/day-019-town-county -k kata               # only tests whose name contains "kata"
pytest phase-2-many-tables/day-019-town-county -x --tb=short         # stop at the first failure, with a short explanation
```

Each test runs one of your files and compares the result with the right answer. A failure shows what came back and what was expected, usually as rows like `('Nakuru', '12')`. From SQL files, every value comes back as text, and `NULL` as `'NULL'`. Read the first failure only, fix it, run again.

**Many tests change the data and run your file a second time**, so an answer typed in by hand, or one that only works for today's rows, fails the second run. If the first run passes and the second fails, your query depends on something it shouldn't (an id you typed, a row's position, a name spelled out).

**Run your work by hand:**

Load a day's data into a practice database, then run your file the way the tests do:

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS practice;"
tools/mysql.sh practice < phase-2-many-tables/day-019-town-county/setup.sql
tools/mysql.sh practice < phase-2-many-tables/day-019-town-county/starter/0-towns_and_counties.sql
```

`tools/mysql.sh practice` on its own opens a `mysql>` prompt in that database: the fastest place to try a query before saving it. If your query changed the data (an `INSERT`, `UPDATE` or `DELETE`), start clean: `tools/mysql.sh -e "DROP DATABASE practice; CREATE DATABASE practice;"` and load `setup.sql` again. The tests always start from a fresh database, so leftovers in yours never affect them.

**Still stuck?** Read the day's "When you're stuck" section first: it lists the mistakes people actually make. Then compare your output with the reference answer's. It spoils the answer, so it's the last resort:

```bash
diff <(tools/mysql.sh practice < phase-2-many-tables/day-019-town-county/starter/0-towns_and_counties.sql) <(tools/mysql.sh practice < phase-2-many-tables/day-019-town-county/solution/0-towns_and_counties.sql)
```

On Windows, run all of this in the Ubuntu (WSL) terminal, not PowerShell: see [WINDOWS.md](../WINDOWS.md).


## Further reading

- [MySQL: JOIN clause](https://dev.mysql.com/doc/refman/8.4/en/join.html) and [subqueries](https://dev.mysql.com/doc/refman/8.4/en/subqueries.html).
- [HackerRank SQL](https://www.hackerrank.com/domains/sql): the Basic Join and Advanced Join sections.
