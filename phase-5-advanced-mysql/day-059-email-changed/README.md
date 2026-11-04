# Day 59: Email Changed

## The brief

Pamoja sends statements to each user's email, but only once they've confirmed it (`valid_email = 1`). Three problems from support:

1. Akinyi changed her email to a typo, and statements went to a stranger. **A changed email must be confirmed again.**
2. `Wanjiku@Pamoja.TEST ` and `wanjiku@pamoja.test` keep ending up as different addresses (Day 53). **Clean every email on the way in.**
3. A fraud case needs every address a user has had. **Keep the history.**

Yesterday's triggers ran *after* a change and touched other tables. Today's mostly run **before** the change and edit the row itself, before it's saved.

## What you'll use

```sql
CREATE TRIGGER clean_email_insert
BEFORE INSERT ON users
FOR EACH ROW
SET NEW.email = LOWER(TRIM(NEW.email));     -- change the row before it's written
```

- **Only a `BEFORE` trigger can change `NEW`.** In an `AFTER` trigger the row is already saved (`ERROR 1362: Updating of NEW row is not allowed in after trigger`). `OLD` can never be changed.
- **`IF NEW.email <> OLD.email`** is how you tell what changed. An `UPDATE` fires the trigger even if it sets a column to the value it already had, or changes a different column.
- **`<>` uses the collation.** With `utf8mb4_0900_ai_ci`, `'WANJIKU@…'` equals `'wanjiku@…'`, so a change of case alone isn't "a change". But spaces count.
- **Several triggers on the same event** run in the order they were created, unless you say otherwise: `FOR EACH ROW PRECEDES other_trigger` or `FOLLOWS other_trigger`. `information_schema.triggers.action_order` shows the order.
- **History tables** are the classic `AFTER UPDATE` job: by then the change has happened, and you know both `OLD` and `NEW`.
- **Refusing with `SIGNAL`** in a `BEFORE DELETE` stops the delete (and the whole statement, if it was deleting many rows).

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS pamoja;"
tools/mysql.sh pamoja < phase-5-advanced-mysql/day-059-email-changed/setup.sql
```

1. `starter/0-reset_valid_email.sql`: a new address must be confirmed again.
2. `starter/1-clean_email.sql`: trim and lower-case on insert and on update. The update one must run *before* `reset_valid_email`.
3. `starter/2-email_history.sql`: record every change of address.
4. `starter/3-keep_verified_users.sql`: confirmed users can't be deleted.
5. `pytest phase-5-advanced-mysql/day-059-email-changed`

## The kata: Rate Limit

In `starter/kata.sql`, write `limit_email_changes`: a user can change their email three times (count their rows in `email_history`), and the fourth change is refused. Other updates (their name, confirming the address) must still work, and so must setting the same address again.

## When you're stuck

- **`ERROR 1362: Updating of NEW row is not allowed in after trigger`**: make it `BEFORE`.
- **Every update resets `valid_email`, even confirming it**: you didn't compare `NEW.email` with `OLD.email`.
- **Wanjiku's `' wanjiku@pamoja.test  '` resets her `valid_email`**: `reset_valid_email` ran first and saw the spaces. Add `PRECEDES reset_valid_email` to `clean_email_update`. It goes between `FOR EACH ROW` and the body.
- **`ERROR 3011: Referenced trigger 'reset_valid_email' for the given action time and event type does not exist`**: `reset_valid_email` has to exist first (step 1).
- **The history gets a row for the name change**: wrap the insert in `IF NEW.email <> OLD.email`.
- **The kata refuses the third change**: three earlier changes are allowed, so refuse when the count is already `>= 3`.
