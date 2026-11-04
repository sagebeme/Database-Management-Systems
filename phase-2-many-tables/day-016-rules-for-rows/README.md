# Day 16: Rules for Rows

## The brief

Yesterday's mess happened because the table let anything in: two phone numbers for one person, rows with no name. A database can enforce rules so that bad rows are refused at the door, whoever's typing and whatever app they're using. These rules are called **constraints**.

Kaimosi Teachers' College is moving its records from spreadsheets into MySQL, and the registrar, Madam Imali, has rules: every student has a name; a member's status is never blank; two customers of the canteen can't share a phone; every product gets its own number automatically; and nobody enrols in the same unit twice. Today you build tables that keep those rules.

## What you'll use

```sql
CREATE TABLE IF NOT EXISTS staff (
    id INT AUTO_INCREMENT PRIMARY KEY,           -- unique, never NULL, numbered for you
    name VARCHAR(100) NOT NULL,                  -- must have a value
    email VARCHAR(100) UNIQUE,                   -- no two rows the same (NULLs allowed)
    role VARCHAR(20) NOT NULL DEFAULT 'teacher'  -- 'teacher' when the INSERT doesn't say
);
```

| Constraint | Promise |
|---|---|
| `NOT NULL` | this column always has a value |
| `DEFAULT x` | if an `INSERT` leaves this column out, use `x` |
| `UNIQUE` | no two rows have the same value here (but several rows may have `NULL`) |
| `PRIMARY KEY` | the column (or columns) that identifies each row: `UNIQUE` + `NOT NULL`, one per table |
| `AUTO_INCREMENT` | MySQL picks the next number for a key column when you don't give one |

- **`DEFAULT` doesn't stop `NULL`.** If someone inserts `NULL` on purpose, the default isn't used. For "never empty, `'active'` unless told otherwise", you need both `NOT NULL` and `DEFAULT 'active'`.
- **A key can be several columns.** In `enrolments`, one student takes many units and one unit has many students, but each *pair* appears once: `PRIMARY KEY (student_id, unit_code)`.
- **`LAST_INSERT_ID()`** returns the id `AUTO_INCREMENT` just gave out on *your* connection. When one `INSERT` adds several rows, it returns the *first* of them.
- **Auto numbers have gaps.** A failed insert or a deleted row uses up a number for good. Never rely on ids being 1, 2, 3 with no holes.

When a constraint says no, MySQL refuses the whole statement:

```
ERROR 1048 (23000): Column 'name' cannot be null
ERROR 1062 (23000): Duplicate entry '254720000001' for key 'customers.phone'
```

## Steps

The tests make an empty database, run your file (twice, to check `IF NOT EXISTS`), then try to insert good and bad rows.

1. `starter/0-students.sql`: `students (adm_no INT, name VARCHAR(100))`, where `name` is required.
2. `starter/1-members.sql`: `members (id INT, name VARCHAR(100), status VARCHAR(10))`, where `status` is never empty and is `'active'` unless an insert says otherwise.
3. `starter/2-customers.sql`: `customers (id INT, name VARCHAR(100), phone VARCHAR(12))`, where no two customers share a phone.
4. `starter/3-products.sql`: `products` with `id` (`INT`, numbered automatically, the primary key), `name` (`VARCHAR(60)`, required) and `price` (`DECIMAL(8, 2)`, required, `0` by default).
5. `starter/4-enrolments.sql`: `enrolments (student_id INT, unit_code CHAR(7), enrolled_on DATE)`, where a student can enrol in a unit only once.
6. `pytest phase-2-many-tables/day-016-rules-for-rows`

## The kata: Which Id?

In `starter/kata.sql`, insert a product called `Kalamu` priced `25`, then print the id MySQL gave it as `new_id`. The test starts the numbering somewhere unexpected, so you can't guess.

## When you're stuck

- **The default test inserts `NULL` and it's accepted**: add `NOT NULL` as well as `DEFAULT`.
- **`ERROR 1075: Incorrect table definition; there can be only one auto column and it must be defined as a key`**: put `PRIMARY KEY` on the `AUTO_INCREMENT` column.
- **`ERROR 1068: Multiple primary key defined`**: a two-column key is one `PRIMARY KEY (a, b)` at the end, not `PRIMARY KEY` on each column.
- **The two customers with no phone are refused**: `UNIQUE` allows any number of `NULL`s. If yours doesn't, you've made `phone` `NOT NULL` or the primary key.
- **The kata prints an old number**: run the `INSERT` before `SELECT LAST_INSERT_ID()`, in the same file (it's per connection).
