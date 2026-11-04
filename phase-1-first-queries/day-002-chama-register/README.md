# Day 2: The Chama Register

## The brief

The Umoja Women's Group in Kakamega has 23 members who each put in money every month. The treasurer, Mama Atieno, keeps a register in a notebook: name, phone number, the day they joined, how much they pledge, and whether they're an official. A second page lists every payment.

In a database, each page becomes a **table**: a grid with named **columns** (what you record) and **rows** (one per member, one per payment). Before any rows go in, you decide each column's **type**, and the database refuses anything that doesn't fit.

Today you build the two empty tables.

**members**

| Column | Type | Why |
|---|---|---|
| `id` | `INT` | a whole number to tell members apart |
| `full_name` | `VARCHAR(100)` | text, up to 100 characters |
| `phone` | `VARCHAR(12)` | like `254712345678`: digits, but not a number you'd add up |
| `joined_on` | `DATE` | a day, written `'2024-03-01'` |
| `monthly_contribution` | `DECIMAL(8, 2)` | money: up to 8 digits, 2 after the point |
| `is_official` | `BOOLEAN` | true or false |

**contributions**

| Column | Type |
|---|---|
| `member_id` | `INT` |
| `amount` | `DECIMAL(10, 2)` |
| `paid_at` | `DATETIME` |
| `mpesa_code` | `CHAR(10)` |

## What you'll use

```sql
CREATE TABLE IF NOT EXISTS savings (
    id INT,
    owner VARCHAR(50),
    balance DECIMAL(10, 2)
);
SHOW TABLES;        -- the tables in the current database
DESCRIBE savings;   -- its columns: Field, Type, Null, Key, Default, Extra
```

The types you need today:

- `INT` for whole numbers (about ±2.1 billion). `TINYINT`, `SMALLINT` and `BIGINT` are smaller and bigger versions.
- `VARCHAR(n)` for text up to *n* characters; `CHAR(n)` for text that's always exactly *n* long, like an M-Pesa code.
- `DECIMAL(p, s)` for money: exact, with *p* digits in all and *s* after the point. Never store money in `FLOAT` or `DOUBLE`, which round in binary: `0.1 + 0.2` comes out as `0.30000000000000004`.
- `DATE` (`'2024-03-01'`), `DATETIME` (`'2024-03-01 14:30:00'`).
- `BOOLEAN`, which MySQL quietly stores as `TINYINT(1)`: `1` for true, `0` for false. `DESCRIBE` shows `tinyint(1)`.

Phone numbers and ID numbers are text even though they're digits: you never add them up, and a leading `0` would vanish from a number.

**`information_schema`** is a built-in database that describes all the others. `information_schema.tables` has one row per table, and `DATABASE()` returns the name of the database you're in.

## Steps

The tests create a fresh, empty database for each test and run your file inside it. To try your files yourself, make a practice database once:

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS chama;"
```

1. `starter/0-list_tables.sql`: list the tables in the current database.
2. `starter/1-members_table.sql`: create `members` exactly as in the table above, columns in that order. Running it twice must not fail.
3. `starter/2-describe_members.sql`: show the columns of `members`.
4. `starter/3-contributions_table.sql`: create `contributions`. Running it twice must not fail.
5. Try them:

   ```bash
   tools/mysql.sh chama < phase-1-first-queries/day-002-chama-register/starter/1-members_table.sql
   tools/mysql.sh chama < phase-1-first-queries/day-002-chama-register/starter/2-describe_members.sql
   ```

6. Run the tests:

   ```bash
   pytest phase-1-first-queries/day-002-chama-register
   ```

## The kata: Table Count

In `starter/kata.sql`, print how many tables the current database has, in a column called `tables`. Count them from `information_schema.tables`, and only the ones in the current database.

## When you're stuck

- **`ERROR 1046: No database selected`**: you ran the file without a database name. Put one after `tools/mysql.sh`.
- **`ERROR 1050: Table 'members' already exists`**: add `IF NOT EXISTS` after `CREATE TABLE`.
- **The test says the types are wrong**: compare with the table above letter by letter. `VARCHAR(12)` isn't `VARCHAR(13)`, and `DECIMAL(8, 2)` isn't `DECIMAL(10, 2)`.
- **You made a mistake and the table already exists**: `DROP TABLE members;` and run your file again.
- **The kata counts too many**: add `WHERE table_schema = DATABASE()`, or you're counting every table on the server.
