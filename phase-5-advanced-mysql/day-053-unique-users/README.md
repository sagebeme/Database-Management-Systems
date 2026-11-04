# Day 53: Unique Users

## The brief

Pamoja is a new chama app. Its first sign-up form had no rules, and Wanjiku signed up three times: as `wanjiku@pamoja.test`, `Wanjiku@Pamoja.test` and `WANJIKU@PAMOJA.TEST ` (with a space). Now the app sends her three statements a month. Phase 5 is MySQL beyond the basics, and it starts where every real system starts: **making the database refuse bad data**, so the app doesn't have to remember to.

You met `CHECK`, `ENUM` and foreign keys on Day 31. Today goes deeper: what `UNIQUE` really compares, adding rules to a table that already has bad rows, and a rule that no plain constraint can say.

## What you'll use

```sql
CREATE TABLE IF NOT EXISTS users (                -- no error if it's already there
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    country ENUM('KE', 'UG', 'TZ') NOT NULL DEFAULT 'KE'
);
```

- **`IF NOT EXISTS` doesn't check the shape.** If a `users` table already exists with different columns, MySQL leaves it alone, with only a note (`SHOW WARNINGS` shows it).
- **`UNIQUE` uses the column's collation.** This course's databases use `utf8mb4_0900_ai_ci`: **a**ccent-**i**nsensitive and **c**ase-**i**nsensitive. So `Wanjiku@Pamoja.test` counts as a duplicate of `wanjiku@pamoja.test`, which is usually what you want for emails. But the `0900` collations don't ignore trailing spaces, so `'a@b.test '` is different from `'a@b.test'`. Trim on the way in.
- **`UNIQUE` allows many `NULL`s**: `NULL` isn't equal to anything, not even another `NULL`.
- **`CHECK` can't use `CURDATE()` or `NOW()`.** A rule must give the same answer whenever it's checked, so "over 18" can't be a `CHECK`. "Born after 1900" can: `CHECK (born_on >= '1900-01-01')`.
- **Adding a rule to a table with bad rows fails**: `ALTER TABLE signups ADD UNIQUE (email)` gives `ERROR 1062` while duplicates remain. Find them, clean them, *then* add the rule.
- **Deleting duplicates with a self-join** (Day 34). Keep the lowest id:

  ```sql
  DELETE s FROM signups AS s
  JOIN signups AS first ON first.email = s.email AND first.id < s.id;
  ```

- **Functional indexes** (MySQL 8.0.13+): a `UNIQUE` index on an *expression*, written in double brackets: `UNIQUE INDEX name ((expression))`. Rows where the expression is `NULL` don't clash with each other.

**`chama_members` rules** (step 3):

| Column | Rules |
|---|---|
| `id` | counts up by itself |
| `chama_id` | required |
| `name` | required; unique within a chama |
| `phone` | required, unique, `^254[17][0-9]{8}$` |
| `born_on` | required, 1900-01-01 or later |
| `role` | `member`, `treasurer`, `secretary` or `chair`; `member` if not given |
| `monthly_contribution` | required, 100 to 100,000 |

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS pamoja;"
tools/mysql.sh pamoja < phase-5-advanced-mysql/day-053-unique-users/setup.sql
```

1. `starter/0-users.sql`: `users`, safe to run twice.
2. `starter/1-country_users.sql`: the same, plus `country`.
3. `starter/2-chama_members.sql`: drop and create `chama_members` with every rule in the table.
4. `starter/3-duplicates.sql`: the addresses used more than once in `signups`.
5. `starter/4-clean_and_lock.sql`: delete the copies, clean the emails, add the `UNIQUE`.
6. `pytest phase-5-advanced-mysql/day-053-unique-users`

## The kata: One Chair per Chama

In `starter/kata.sql`, change `chama_members` (with `ALTER TABLE`) so a chama can't have two chairs. A plain `UNIQUE (chama_id, role)` won't do: it would also stop two ordinary members. Think about an expression that is the `chama_id` for chairs and `NULL` for everyone else.

## When you're stuck

- **Running `0-users.sql` twice gives `ERROR 1050: Table 'users' already exists`**: `CREATE TABLE IF NOT EXISTS`.
- **`'NG'` went into `country`**: it shouldn't, in strict mode. If it went in as `''`, your server isn't in strict mode; the course databases are.
- **`ERROR 3814: An expression of a check constraint 'chama_members_chk_2' contains disallowed function: curdate`**: use a fixed date.
- **`3-duplicates.sql` counts Wanjiku twice, not three times**: group by `LOWER(TRIM(email))`, not by `email`.
- **`ERROR 1062` on the `ALTER TABLE`**: some copies survived. Delete *before* you update, comparing `LOWER(TRIM(...))` in the join, so the first sign-up is the one that's kept.
- **`ERROR 1093: You can't specify target table 'signups' for update in FROM clause`**: that's `DELETE ... WHERE id IN (SELECT ... FROM signups)`. Use the multi-table `DELETE s FROM signups AS s JOIN signups AS first ...`.
- **The kata's index gives `ERROR 1064` near `CASE`**: a functional index's expression needs its own brackets: `((CASE ... END))`.
