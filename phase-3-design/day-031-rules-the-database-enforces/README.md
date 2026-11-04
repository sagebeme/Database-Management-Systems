# Day 31: Rules the Database Enforces

## The brief

A boda boda sacco in Kisumu is moving its records off paper. The chairman's worry is the mess the old system allowed: a rider registered aged 12, a bike assigned to a rider who left two years ago, a trip with a fare of minus 50 shillings, and a trip that "ended" before it started.

Those are all **integrity** failures: data that breaks a rule about what makes sense. Day 29's Python had to check every rule by hand, in every program. Today you write the rules into the tables, once, and the database refuses anything that breaks them, whichever app or person sends it.

## What you'll use

Exam questions sort integrity rules into four kinds:

| Kind | The rule | In SQL |
|---|---|---|
| **Domain** | each value comes from the allowed set: the right type, the right range | column types, `NOT NULL`, `CHECK`, `ENUM` (Day 53) |
| **Entity** | every row can be identified: the primary key is never `NULL` | `PRIMARY KEY` |
| **Key** | no two rows share a candidate key | `PRIMARY KEY`, `UNIQUE` |
| **Referential** | a foreign key matches a real row in the table it points at, or is `NULL` | `FOREIGN KEY ... REFERENCES` |

**`CHECK`** states a rule for each row. MySQL enforces it from 8.0.16 on; older versions read it and ignored it.

```sql
age TINYINT NOT NULL CHECK (age BETWEEN 18 AND 70),            -- on one column
CHECK (ended_at IS NULL OR ended_at > started_at),            -- across columns, at the end
CONSTRAINT phone_format CHECK (phone REGEXP '^2547[0-9]{8}$') -- with a name of your choosing
```

A `CHECK` passes when its condition is true **or unknown**, so a `NULL` phone passes `phone REGEXP ...` (Day 11's three-valued logic). If `NULL` should fail too, add `NOT NULL`.

**What happens to the children** when the parent row changes:

```sql
FOREIGN KEY (rider_id) REFERENCES riders (id)
    ON DELETE SET NULL      -- the rider leaves: keep the bike, with no rider
    ON UPDATE CASCADE       -- the rider's id changes: the bike follows
```

| Action | On parent `DELETE` | On parent key `UPDATE` |
|---|---|---|
| `RESTRICT` / `NO ACTION` (the default) | refuse | refuse |
| `CASCADE` | delete the children | change the children's foreign key too |
| `SET NULL` | set the children's foreign key to `NULL` | the same |

Name your constraints (`CONSTRAINT phone_format CHECK ...`), and error messages tell you which rule failed: `Check constraint 'phone_format' is violated.`

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS boda;"
```

1. `starter/0-riders.sql`: `riders`: `id` (auto-numbered primary key), `name` (`VARCHAR(60)`, required), `licence_no` (`CHAR(9)`, required, unique), `age` (`TINYINT`, required, 18 to 70).
2. `starter/1-bikes.sql`: `bikes`: `plate` (`VARCHAR(10)`, primary key), `rider_id` (optional, a real rider), `engine_cc` (`SMALLINT`, required, 50 to 1000). A deleted rider's bikes stay, with no rider; if a rider's id changes, their bikes follow.
3. `starter/2-trips.sql`: `trips`: `id` (auto-numbered primary key), `plate` (required, a real bike), `fare` (`INT`, required, above 0), `started_at` (`DATETIME`, required), `ended_at` (`DATETIME`, optional, after `started_at`). Deleting a bike deletes its trips; a changed plate changes its trips' plate.
4. `starter/answers.py`: which kind of integrity does each mistake break?
5. `pytest phase-3-design/day-031-rules-the-database-enforces`

## The kata: Name the Rule

In `starter/kata.sql`, add an optional `phone` (`CHAR(12)`) to `riders`, with a `CHECK` constraint called `phone_format`: when given, a phone is `2547` or `2541` followed by 8 digits.

## When you're stuck

- **`ERROR 3819: Check constraint 'riders_chk_1' is violated`**: that's your rule working. Name the constraint and the message names it too.
- **`ERROR 3823: Column 'rider_id' cannot be used in a check constraint ... needed in a foreign key constraint ... referential action`**: a column that `ON DELETE`/`ON UPDATE` can change can't also be in a `CHECK`. Drop the `CHECK` on `rider_id`; the foreign key already guards it.
- **A rule that needs another table** ("a rider has at most 2 bikes"): a `CHECK` sees only the row being written. Rules across rows or tables need a trigger (Day 58).
- **`ERROR 1830: Column 'rider_id' cannot be NOT NULL: needed in a foreign key constraint SET NULL`**: `ON DELETE SET NULL` needs a column that allows `NULL`.
- **The trip that ends before it starts is accepted**: the cross-column `CHECK` goes after the columns, as its own line.
- **The `REGEXP` accepts `+254...`**: anchor both ends: `^...$`.
