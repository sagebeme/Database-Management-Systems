# Day 42: Does It Depend?

## The brief

Yesterday you split the tuition spreadsheet by eye: "the room depends on the tutor". Today that sentence gets a precise meaning, the **functional dependency**, which every normal form from Day 48 on is built from.

A stage clerk in Nairobi logs matatu trips: plate, sacco, route, driver, fare, date. The sacco manager says "a vehicle belongs to one sacco" and "a route has one fare". Those are functional dependencies, and you can check them against the log. One of them is broken by a typo.

## What you'll use

**X → Y** ("X determines Y", "Y depends on X") means: any two rows that agree on X also agree on Y. Knowing X, there's only one possible Y.

```
plate     sacco               plate → sacco holds if no plate ever appears
KDA 101A  Mwangaza Shuttle    with two different saccos
KDB 202B  Pwani Express
KDB 202B  Pwani Expres        <- two saccos for one plate: it fails (here, a typo)
```

- **Trivial**: Y ⊆ X, like `AB → A`. Always true, says nothing.
- **Non-trivial**: Y has something not in X.
- **A key determines everything**: if X is a key, X → every attribute. (That's what a key *is*, in FD terms.)
- **Direction matters**: `tutor → room` doesn't give `room → tutor`; a room can host several tutors.

**FDs are rules about meaning, like keys** (Day 30). The data can show an FD **fails** (one counterexample is enough), but it can't prove one **holds**: the log may simply not have hit the exception yet. Decide FDs from how the business works, then use the data to catch mistakes.

**Checking an FD in SQL**: group by the left side and count the distinct right sides.

```sql
SELECT plate, COUNT(DISTINCT sacco) AS saccos
FROM trips GROUP BY plate HAVING COUNT(DISTINCT sacco) > 1;   -- empty means plate → sacco holds
```

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS stage;"
tools/mysql.sh stage < phase-4-normalisation/day-042-does-it-depend/setup.sql
```

1. `starter/fd_check.py`, `is_trivial`.
2. `holds`: walk the rows, remembering the right-side value seen for each left-side value. A second, different one means it fails.
3. `violations`: the left-side values that break it.
4. `starter/0-plate_sacco_violations.sql`: plates with more than one sacco: `plate`, `saccos`.
5. `starter/1-route_fare_holds.sql`: one value, `holds`: 1 if `route → fare` holds, else 0.
6. `starter/answers.py`.
7. `pytest phase-4-normalisation/day-042-does-it-depend`

## The kata: Find Them All

In `starter/fd_check.py`, write `holding_fds`: every non-trivial FD with one attribute on the right and one or two on the left that holds in the rows, keeping only minimal left sides. This is FD *discovery*, which tools use to suggest keys and normal forms from data. On the test's five rows it finds `subject → tutor` (a real rule) but also `(student, room) → subject`, which is only true because this sample is small. Data suggests FDs; people decide them.

## When you're stuck

- **`holds` with several attributes**: build a tuple of the left values (`tuple(row[a] for a in lhs)`) as a dict key, and a tuple of the right values to compare.
- **`holds([], ...)`**: no rows means no counterexample, so `True`.
- **The SQL counts 2 saccos for every plate**: count `DISTINCT sacco`, not rows.
- **`1-route_fare_holds.sql` returns several rows**: wrap the group query as a derived table and count *its* rows: zero broken routes means it holds.
- **The kata includes `(("subject", "tutor"), "room")`**: `subject` alone already determines `room`, so the pair isn't minimal.
