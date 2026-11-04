# Day 1: Hello, MySQL

## The brief

Mama Wanjiru sells vegetables at Githurai market. Her records are an exercise book: who owes her, what she bought from the farmers at Wakulima, what sold. The book gets wet, the pages tear, and finding last month's debts means flipping through everything.

A **database** is that exercise book done properly: organised, searchable, shared safely by many people at once. A **database server** such as MySQL keeps many databases, one per app or business. Today you meet the server and make Mama Wanjiru's database.

```
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
```

The four you see are MySQL's own. You'll add `mama_mboga`.

## What you'll use

- **SQL** (Structured Query Language): the language every relational database speaks. A statement ends with `;`. Keywords aren't case-sensitive, but writing them in capitals makes them easy to spot.
- `SHOW DATABASES;` lists the databases.
- `CREATE DATABASE name;` makes one. `CREATE DATABASE IF NOT EXISTS name;` does nothing, instead of failing, when it's already there.
- `DROP DATABASE name;` deletes one, with everything in it, immediately and without asking. `DROP DATABASE IF EXISTS name;` doesn't fail when it's already gone.
- `SELECT` with no table works out a value: `SELECT 7 * 6 AS answer;` prints a column called `answer` holding `42`.

`IF NOT EXISTS` and `IF EXISTS` make a script **idempotent**: you can run it twice and get the same result. Setup scripts in real projects are written this way, because they get re-run.

## Steps

If you haven't set up yet, follow **Setting up** in the main README (start the databases with `tools/devdb.sh up`).

1. Open a MySQL prompt and look around:

   ```bash
   tools/mysql.sh
   ```

   Type `SHOW DATABASES;` and press Enter. Leave with `exit`.

2. In `starter/0-list_databases.sql`, write the statement that lists every database.
3. In `starter/1-create_database_if_missing.sql`, create `mama_mboga` so that running the file twice is not an error.
4. In `starter/2-remove_database.sql`, delete `mama_mboga` so that running it when the database is already gone is not an error.
5. Run each file the way the tests do, by feeding it to the client:

   ```bash
   tools/mysql.sh < phase-1-first-queries/day-001-hello-mysql/starter/1-create_database_if_missing.sql
   tools/mysql.sh -e "SHOW DATABASES;"
   ```

6. Run the tests:

   ```bash
   pytest phase-1-first-queries/day-001-hello-mysql
   ```

   Every line should end in `PASSED` (or the summary should say `6 passed`). A failure shows what your file printed next to what was expected.

## The kata: Till Maths

Every day ends with a short puzzle. Today's: 3 bunches of sukuma at 20 bob and 2 kg of tomatoes at 120 bob a kilo. In `starter/kata.sql`, print the total in a column called `total`, using one `SELECT` and arithmetic (`+`, `*`), not the number you worked out in your head.

## When you're stuck

- **`ERROR 2003: Can't connect to MySQL server`**: the server isn't running. `tools/devdb.sh up`, then `tools/devdb.sh status`.
- **`ERROR 1007: Can't create database 'mama_mboga'; database exists`**: add `IF NOT EXISTS`.
- **`ERROR 1008: Can't drop database 'mama_mboga'; database doesn't exist`**: add `IF EXISTS`.
- **The prompt shows `->` and waits**: you forgot the `;`. Type it and press Enter.
- **The kata says the column is wrong**: the name comes from `AS total`. Without it, MySQL names the column after the expression.
- **Still stuck?** Read the file in `solution/`, close it, and write your own from memory.
