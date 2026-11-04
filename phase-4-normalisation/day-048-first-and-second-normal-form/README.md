# Day 48: First and Second Normal Form

## The brief

Normal forms are a ladder of tests. Each one rules out a specific way a table can store a fact twice, and each rung includes the ones below:

```
1NF  ⊃  2NF  ⊃  3NF  ⊃  BCNF  ⊃  4NF      (every BCNF table is also 3NF, 2NF and 1NF)
```

Today, the first two rungs. A chama's member list arrived with several phone numbers squeezed into one cell, which breaks **1NF**. And a college's `(student, course, name, fee, grade)` table repeats every student's name in every course they take, which breaks **2NF**.

## What you'll use

**First normal form**: every value is **atomic**, a single value from its domain. No lists in a cell, no repeating columns (`phone1, phone2, phone3`). The fix: one row per value, in a table of its own (a multivalued attribute's table, Day 32).

```
members_raw                         member_phones
id  name     phones                 member_id  phone
1   Wanjiku  254711..., 254722...   1          254711000001
                                    1          254722000001
```

Splitting a list in SQL: turn `'a, b, c'` into the JSON array `["a"," b"," c"]`, and `JSON_TABLE` returns one row per element (Day 63 covers JSON properly):

```sql
SELECT m.id, TRIM(j.phone)
FROM members_raw AS m,
     JSON_TABLE(CONCAT('["', REPLACE(m.phones, ',', '","'), '"]'),
                '$[*]' COLUMNS (phone VARCHAR(20) PATH '$')) AS j;
```

**Second normal form**: 1NF, and **no non-prime attribute depends on part of a candidate key**.

- *Prime* attributes are in some candidate key; *non-prime* are in none (Day 43).
- A **partial dependency** is X → A where X is a **proper subset** of a candidate key and A is non-prime.

```
R(student, course, name, fee, grade),  key {student, course}
student → name     partial: name depends on half the key
course  → fee      partial
student, course → grade   fine: the whole key
```

The fix: move each partial dependency into its own table, `(student, name)` and `(course, fee)`, and keep `(student, course, grade)`. That's lossless, because the common attribute is the key of each new table (Day 46).

Two shortcuts: a relation whose candidate keys are all **single attributes** is automatically in 2NF (there's no proper part to depend on). And 2NF says nothing about prime attributes.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS chama;"
tools/mysql.sh chama < phase-4-normalisation/day-048-first-and-second-normal-form/setup.sql
```

1. `starter/0-member_phones.sql`: `member_phones(member_id → members_raw, phone CHAR(12))`, keyed on the pair, filled with one trimmed row per phone.
2. `starter/1-phones_per_member.sql`: every member's `name` and number of `phones`, zero included. Most first, ties alphabetical.
3. `starter/2-who_owns_this.sql`: who owns 254744000003? `name`. Try writing this against `members_raw` with `LIKE`, then see why 1NF is better.
4. `starter/second_nf.py`: `non_prime`, `partial_dependencies`, `is_2nf`. Closure and candidate keys are given.
5. `starter/answers.py`.
6. `pytest phase-4-normalisation/day-048-first-and-second-normal-form`

## The kata: Pull Them Out

In `starter/second_nf.py`, write `to_2nf`: move each partial dependency out into its own part, and leave the rest (with the key) as the main part.

## When you're stuck

- **The phones keep their spaces**: `TRIM(j.phone)`.
- **Mutua causes an error**: his `phones` is `NULL`, so the JSON is `NULL` and `JSON_TABLE` gives no rows. That's right: no phones.
- **`partial_dependencies` lists `(student, course) → grade`**: X must be a *proper* subset of the key: sizes 1 to len(key) − 1.
- **`AB->C; C->B` counts as partial**: the keys are AB and AC, so B is prime, and C → B isn't a partial dependency. Only non-prime attributes count.
- **`to_2nf` repeats an attribute in two parts**: once an attribute has moved out, don't move it again.
