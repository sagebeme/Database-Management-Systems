# Day 79: PostgreSQL for MySQL Users

## The brief

A matatu sacco's new booking app runs on **PostgreSQL**, and so do many of the jobs you'll apply for. Everything from Phases 1 to 6 carries over: tables, keys, joins, `GROUP BY`, indexes, transactions. What changes is the accent: a different client, stricter types, a few new words, and some features MySQL doesn't have.

Today you'll find your way around `psql` and write the Postgres way of the things you already know: auto-numbered ids, schemas, getting new ids back, and "insert or update".

## What you'll use

**The client**: `psql`. Commands that start with a backslash belong to `psql` itself, not to SQL:

| MySQL | psql |
|---|---|
| `SHOW DATABASES;` | `\l` |
| `USE matatu;` | `\c matatu` |
| `SHOW TABLES;` | `\dt` |
| `DESCRIBE routes;` | `\d routes` |
| `exit` | `\q` |

`\?` lists them all; `\h CREATE TABLE` shows SQL help.

**Differences you'll hit in the first hour**:

| | MySQL | PostgreSQL |
|---|---|---|
| Auto-numbered id | `INT AUTO_INCREMENT` | `INT GENERATED ALWAYS AS IDENTITY` (or `BY DEFAULT`, which lets you set it by hand) |
| Strings | `VARCHAR(n)`, quotes `'` or `"` | `TEXT` is normal; only `'` quotes strings; `"` quotes *names* |
| Case-insensitive match | `LIKE` (with the usual collations) | `LIKE` is case-sensitive; use `ILIKE` |
| Joining strings | `CONCAT(a, b)`, `GROUP_CONCAT` | `a || b`, `string_agg(x, ', ' ORDER BY x)` |
| Insert or update | `INSERT ... ON DUPLICATE KEY UPDATE` | `INSERT ... ON CONFLICT (col) DO UPDATE SET col = EXCLUDED.col` |
| The new id | `LAST_INSERT_ID()` | `INSERT ... RETURNING id` (any columns, any number of rows) |
| Booleans | `TINYINT(1)` | real `BOOLEAN`, shown as `t` / `f` |
| Casting | `CAST(x AS SIGNED)` | `CAST(x AS INT)` or `x::int` |

**Schemas**: in MySQL, "database" and "schema" mean the same thing. In Postgres, a database holds **schemas**, and a schema holds tables and views. Everything you've made so far went into the schema `public`. `CREATE SCHEMA reports;` makes another, and `reports.route_fares` names a view in it. Teams use schemas to keep parts of an app apart, and to grant access to one part only (Day 94).

**DDL is transactional**: `BEGIN; CREATE TABLE ...; ROLLBACK;` really undoes the `CREATE`. MySQL commits DDL immediately. That will matter for migrations (Day 82).

## Steps

```bash
tools/psql.sh postgres -c "CREATE DATABASE matatu;"
tools/psql.sh matatu -f phase-7-beyond-mysql/day-079-postgresql-for-mysql-users/setup.sql
tools/psql.sh matatu
```

Explore with `\dt`, `\d routes` and `\d saccos`. Then:

1. `starter/0-stages.sql`: the `stages` table, with an identity column.
2. `starter/1-reports_schema.sql`: the `reports` schema and its `route_fares` view.
3. `starter/2-returning.sql`: add a sacco and get its id back in the same statement.
4. `starter/3-upsert.sql`: add route 44, or update it if it's there. It must be safe to run twice.
5. `starter/4-rongai.sql`: routes to anywhere called Rongai, in any capitals.
6. `starter/answers.py`: the `psql` commands. The tests run them.
7. `pytest phase-7-beyond-mysql/day-079-postgresql-for-mysql-users`

## The kata: Every Sacco's Routes

In `starter/kata.sql`, list each sacco with its route numbers joined into one string, in order, including saccos with no routes. MySQL's `GROUP_CONCAT` is Postgres's `string_agg`.

## When you're stuck

- **`ERROR: cannot insert a non-DEFAULT value into column "id"`**: that's `GENERATED ALWAYS` doing its job. Leave `id` out of the column list.
- **`ERROR: column "Rongai" does not exist`**: double quotes mean a *name* in Postgres. Strings take single quotes.
- **`ERROR: relation "route_fares" does not exist`** when you query the view: it's in `reports`, so write `reports.route_fares`.
- **The upsert says `there is no unique or exclusion constraint matching the ON CONFLICT specification`**: `ON CONFLICT (number)` needs a unique constraint on `number`, which `routes` has. Check the column name.
- **`EXCLUDED`**: it's the row you tried to insert. `SET fare = EXCLUDED.fare` copies the new fare over the old.
- **The kata sorts `19C` after `58`**: `ORDER BY number` goes *inside* `string_agg(...)`. Route numbers are text, so `'237'` comes before `'58'`.
