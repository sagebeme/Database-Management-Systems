# Day 24: Changing the Shape

## The brief

The first version of the Riverwood Plus app went live in a hurry. Now Brenda's developers have a list of changes: subscribers need an email column; every subscriber must have a plan; `phone` should be called `msisdn`, like everywhere else in the telecom world; the session log needs clearing before launch; an old promo table has to go; and `name` only holds 20 characters, which Nyokabi Wairimu Kamau-Ndung'u wa Mathenge has already found out.

You can change a table that already holds data. It just needs more care than creating one, because the rows already in it have to fit the new rules.

## What you'll use

```sql
ALTER TABLE t ADD COLUMN c VARCHAR(50) NULL AFTER other;   -- or FIRST; the end is the default
ALTER TABLE t MODIFY c VARCHAR(80) NOT NULL DEFAULT 'x';   -- new definition, same name
ALTER TABLE t RENAME COLUMN old TO new;                     -- same definition, new name
ALTER TABLE t DROP COLUMN c;
ALTER TABLE t RENAME TO new_name;
```

- **`MODIFY` replaces the whole definition.** Anything you don't say again is gone. Widening `name VARCHAR(20) NOT NULL` with `MODIFY name VARCHAR(100)` quietly makes it nullable. Say `NOT NULL` again.
- **The data must fit first.** `NOT NULL` on a column that already holds `NULL`s fails with `Invalid use of NULL value`. Fix the rows with an `UPDATE`, then change the column. Shrinking `VARCHAR(100)` to `VARCHAR(10)` fails with `Data truncated` if any value is longer.
- **`DESCRIBE t;`** (or `SHOW CREATE TABLE t;`) shows a table's shape before and after.

Three ways to remove things:

| Statement | Removes | Ids restart? | Can be filtered? | Undo in a transaction? |
|---|---|---|---|---|
| `DELETE FROM t WHERE ...` | the rows you pick | no | yes | yes (Day 65) |
| `TRUNCATE TABLE t` | every row, fast | yes | no | no |
| `DROP TABLE t` | the table itself | (no table) | no | no |

`DROP TABLE IF EXISTS t` doesn't fail when `t` is already gone, which makes a script safe to run twice. A `TRUNCATE` or `DROP` is permanent, so look at what you're about to remove first.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS riverwood;"
tools/mysql.sh riverwood < phase-2-many-tables/day-024-changing-the-shape/setup.sql
```

Each test starts again from `setup.sql` and runs one file. At your prompt, reload `setup.sql` between steps.

1. `starter/0-add_email.sql`: add `email` (`VARCHAR(100)`, optional) to `subscribers`, right after `name`.
2. `starter/1-plan_required.sql`: `plan` must never be empty and is `'basic'` unless an insert says otherwise. Two subscribers have no plan yet: give them `'basic'` first.
3. `starter/2-rename_phone.sql`: rename `phone` to `msisdn`.
4. `starter/3-clear_session_log.sql`: empty `session_log` so its ids start again from 1.
5. `starter/4-drop_old_promos.sql`: remove `old_promo_codes`. The file must work twice.
6. `pytest phase-2-many-tables/day-024-changing-the-shape`

## The kata: Room for Long Names

In `starter/kata.sql`, widen `subscribers.name` to `VARCHAR(100)`. It must still be required.

## When you're stuck

- **`ERROR 1138: Invalid use of NULL value`**: rows already hold `NULL`. Run the `UPDATE` before the `ALTER`, in the same file.
- **The new subscriber gets `NULL` instead of `'basic'`**: `MODIFY` needs `DEFAULT 'basic'` as well as `NOT NULL`.
- **The first insert in the log gets id 7**: `DELETE FROM session_log` keeps counting. `TRUNCATE` starts again.
- **The kata test inserts a `NULL` name and it works**: your `MODIFY` dropped `NOT NULL`. Restate it.
- **`ERROR 1051: Unknown table`** on the second run: `DROP TABLE IF EXISTS`.
