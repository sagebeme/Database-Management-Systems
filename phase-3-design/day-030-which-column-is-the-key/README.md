# Day 30: Which Column Is the Key?

## The brief

The Matatu Owners' registry is going digital, and the first argument at the planning meeting is about keys. Is a vehicle identified by its number plate, or by its chassis number? Both are unique. What about the sacco, route and seats together? In the sample spreadsheet no two vehicles share all three, but is that a rule, or luck?

You've used `PRIMARY KEY` since Day 16. Today you learn the vocabulary exam questions use, and the one fact that settles the argument: **a key is a rule about what the data means, not something you discover from the rows.**

## What you'll use

For a relation (table) R:

| Term | Meaning | Matatu example |
|---|---|---|
| **Superkey** | any set of attributes whose values are never the same in two rows | `{reg_no}`, `{reg_no, seats}`, ... |
| **Candidate key** | a *minimal* superkey: remove any attribute and it stops being one | `{reg_no}`, `{chassis_no}` |
| **Primary key** | the candidate key you choose to identify rows. One per table, never `NULL` | `reg_no` |
| **Alternate key** | the other candidate keys. Make them `UNIQUE NOT NULL` | `chassis_no` |
| **Foreign key** | attributes that must match a key in another table (or be `NULL`) | `sacco_id` |
| **Prime attribute** | an attribute in at least one candidate key (Phase 4 needs this) | `reg_no`, `chassis_no` |
| **Composite key** | a key made of more than one attribute | `(student_id, unit_code)` on Day 16 |

**Data can disprove a key, but never prove one.** Two rows sharing a value show it isn't a key. Five rows that happen to differ prove nothing: `{sacco, route, seats}` is unique in today's sample, but the sixth matatu could break it. You decide keys from meaning ("every vehicle has its own plate, by law"), and the sample is only a check.

**Counting superkeys** is a favourite exam question. If R has n attributes and one candidate key of k attributes, every superkey is that key plus any subset of the other n − k, so there are 2^(n−k). With several candidate keys, add the counts for each, then subtract the sets you counted twice (**inclusion–exclusion**):

```
R(A, B, C, D), candidate keys {A} and {B, C}
contain A:          2^3 = 8
contain B, C:       2^2 = 4
contain A, B and C: 2^1 = 2   (counted in both)
superkeys = 8 + 4 − 2 = 10
```

With three keys: |K1| + |K2| + |K3| − |K1∩K2| − |K1∩K3| − |K2∩K3| + |K1∩K2∩K3|, where each term is 2^(attributes left over).

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS fleet;"
tools/mysql.sh fleet < phase-3-design/day-030-which-column-is-the-key/setup.sql
```

1. `starter/keys.py`, `unique_on`: are these columns unique across the rows?
2. `starter/keys.py`, `could_be_keys`: every minimal unique set of columns. Try sizes 1, 2, 3, ... with `itertools.combinations`, and skip any set containing a key you've already found.
3. `starter/keys.py`, `count_superkeys`: inclusion–exclusion, without listing the sets.
4. `starter/answers.py`: replace each `None`.
5. `starter/0-vehicles.sql`: the `vehicles` table, with its primary key, alternate key and foreign key.
6. `pytest phase-3-design/day-030-which-column-is-the-key`

## The kata: Every Superkey

In `starter/keys.py`, write `all_superkeys`, which lists every superkey (smallest first). Check that its length matches `count_superkeys` for a few examples.

## When you're stuck

- **`could_be_keys` returns `("reg_no", "seats")`**: that contains `("reg_no",)`, which you'd already found. It's a superkey, not a candidate key.
- **`count_superkeys` is too big**: you counted the sets that contain two keys twice. Subtract them.
- **Which power of 2 for "contains both keys"?** Take the union of the keys: `{A} ∪ {B, C}` = `{A, B, C}` leaves one attribute free, so `2^(4−3)` = 2 sets.
- **The alternate key accepts `NULL`**: `UNIQUE` allows `NULL`s (Day 16). Add `NOT NULL`.
