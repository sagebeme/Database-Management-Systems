# Day 37: Relational Algebra II

## The brief

The college registrar has a question that sounds simple: **which first-years have registered for *every* core unit?** They can't sit exams otherwise. "Some core unit" is an easy join. "Every" is harder, and the algebra has a dedicated operator for it: **division**. GATE asks about division nearly every year.

Today: the joins as algebra (they're all built from Day 36's six operators), then division, in Python and in SQL.

## What you'll use

| Operator | Symbol | Means | Built from |
|---|---|---|---|
| natural join | R ⋈ S | pair tuples that agree on every shared attribute; keep shared attributes once | × σ π |
| theta join | R ⋈<sub>θ</sub> S | pairs where condition θ holds | σ<sub>θ</sub>(R × S) |
| equi-join | R ⋈<sub>R.a=S.b</sub> S | a theta join whose θ is only `=` | σ(R × S) |
| left outer join | R ⟕ S | the join, plus unmatched R tuples padded with NULL | ⋈ ∪ − × |
| semi-join | R ⋉ S | tuples of R that match something in S (R's attributes only) | π<sub>R</sub>(R ⋈ S) |
| division | R ÷ S | values in R paired with **every** tuple of S | π − × (below) |

**Division**, with R(adm_no, code) and S(code) = the core units:

```
R                 S           R ÷ S
adm_no  code      code        adm_no
S0001   COM101    COM101      S0001     Achieng has all three
S0001   COM102    COM102      S0003     Chebet has all three
S0001   MAT101    MAT101
S0002   COM101                (Baraka lacks COM102; Duncan has none)
...
```

In basic operators, with A = R's attributes that aren't in S:

```
R ÷ S  =  π_A(R)  −  π_A( (π_A(R) × S)  −  R )
          everyone   everyone paired with every unit, minus what they really took
                     = the pairs that are MISSING; their A values are the ones to drop
```

**Division in SQL.** SQL has no `DIVIDE`. "Took every core unit" means "there is **no** core unit they did **not** take": two `NOT EXISTS`, one inside the other.

```sql
WHERE NOT EXISTS (                    -- there's no core unit u ...
    SELECT 1 FROM units u WHERE u.core
      AND NOT EXISTS (                -- ... that this student didn't register for
          SELECT 1 FROM registrations r WHERE r.adm_no = s.adm_no AND r.code = u.code))
```

Or count: students whose number of core registrations equals the number of core units. Counting is easier to read, but it relies on `(adm_no, code)` being a key; with duplicate rows, the count lies.

**Careful with "every" and nothing.** If S is empty, *every* A value in R qualifies (there's nothing to miss). That's correct logic ("all zero units taken"), but sometimes surprising.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS college;"
tools/mysql.sh college < phase-3-design/day-037-relational-algebra-ii/setup.sql
```

1. `starter/algebra.py`: `natural_join`, `theta_join`, `left_outer_join`, `semi_join`.
2. `divide`: for each candidate value of r's other attributes, check it appears with every tuple of s.
3. `starter/0-every_core_unit.sql`: names of students registered for every core unit, with two `NOT EXISTS`. Alphabetical.
4. `starter/1-every_core_unit_by_counting.sql`: the same, by counting.
5. `starter/answers.py`.
6. `pytest phase-3-design/day-037-relational-algebra-ii`

## The kata: Division the Hard Way

In `starter/algebra.py`, write `divide_with_basics` using only the formula above and the helpers `_project`, `_product` and `_minus` (Day 36's operators, finished).

## When you're stuck

- **`natural_join` repeats the shared column**: keep s's attributes that r *doesn't* have, and only those.
- **`left_outer_join` loses Esther**: after joining, find r's tuples that matched nothing and add them with `None` for each of s's extra attributes.
- **`divide` returns students who took *any* core unit**: you joined. For each student, check *every* core unit is among theirs.
- **The SQL division returns everyone**: the inner `NOT EXISTS` must tie both to the outer student (`r.adm_no = s.adm_no`) and to the unit (`r.code = u.code`).
- **The counting version counts ENG110 too**: join to `units` with `u.core`, so only core units count.
