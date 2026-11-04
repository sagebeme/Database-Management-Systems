# Day 47: Splitting Without Forgetting

## The brief

A courier in the Rift Valley divides towns into delivery zones. The rules: each zone is in one town (`zone → town`), and a street in a town is in exactly one zone (`street, town → zone`). To fix an anomaly, the developer splits `addresses(street, town, zone)` into `zones(zone, town)` and `addresses(street, zone)`. The split is lossless. But now the rule "a street in a town has one zone" lives in **no single table**. The database can't check it with a key or constraint. Someone records Kenyatta Avenue, Nakuru in two zones, and nothing objects.

A split that keeps every FD checkable inside a single table is **dependency preserving**. It's the second thing to want from a split, after losslessness. And sometimes (tomorrow's BCNF) you can't have both.

## What you'll use

A decomposition into R₁, ..., Rₙ **preserves** F if the FDs that hold inside each Rᵢ, taken together, imply all of F. Then each table's keys and constraints enforce the rules on their own, with no joins.

**Projected FDs.** The FDs "inside" Rᵢ aren't just the ones in F whose attributes all fit. They're everything F *implies* within Rᵢ. That's why, with F = {A → B, B → C, C → D, D → A} split into AB, BC, CD, the rule D → A isn't lost: CD knows D → C, BC knows C → B, AB knows B → A, and together they give D → A.

**The fast test for one FD X → Y** (no need to list projections, which can be exponential):

```
Z = X
repeat until Z stops growing:
    for each part Ri:
        Z = Z ∪ ( (Z ∩ Ri)⁺ ∩ Ri )        (closure under all of F)
X → Y is preserved  if  Y ⊆ Z
```

Each step asks "what can table Rᵢ alone work out from what we know so far?"

**Lost FDs can only be checked by joining**, which in SQL means a query (or a trigger) instead of a constraint:

```sql
SELECT a.street, z.town, COUNT(*) FROM addresses a JOIN zones z ON z.zone = a.zone
GROUP BY a.street, z.town HAVING COUNT(*) > 1;     -- the lost rule's violations
```

| | Lossless? | Dependency preserving? |
|---|---|---|
| Always possible for 3NF | yes | yes (Day 49's synthesis) |
| Always possible for BCNF | yes | **not always** |

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS courier;"
```

1. `starter/preserve.py`, `preserved`: the fast test for one FD.
2. `is_dependency_preserving` and `lost`.
3. `starter/0-zone_tables.sql`: `zones(zone CHAR(3) PK, town)` and `addresses(street, zone → zones)` with the pair as the key.
4. `starter/1-broken_rule.sql`: where `(street, town) → zone` is broken: `street`, `town`, `zones`.
5. `starter/answers.py`.
6. `pytest phase-4-normalisation/day-047-splitting-without-forgetting`

## The kata: What Each Table Knows

In `starter/preserve.py`, write `project_fds(fds, part)`: the FDs that hold inside one part, found by closing every subset of it. It's exponential in the part's size, which is why the fast test exists, but it shows you exactly what each table can enforce.

## When you're stuck

- **`preserved` says D → A is lost**: one pass over the parts isn't enough. Keep looping over all the parts until Z stops growing.
- **The closure must use all of F**: `(Z ∩ Ri)⁺` is computed with the full FD set, then cut back to Ri's attributes.
- **`1-broken_rule.sql` finds nothing after the bad insert**: group by street *and* the zone's town (from the join), not by zone.
- **`project_fds` returns `AC → C`**: subtract X from what it gives; trivial parts don't count.
