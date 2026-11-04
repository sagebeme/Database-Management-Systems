# Day 69: As If One at a Time

## The brief

Running transactions one after another (a **serial schedule**) is always correct, and painfully slow. Interleaving them is fast, and sometimes wrong. So when is an interleaving *safe*? When it gives the same result as **some** serial order. Then it's **serializable**, and nobody can tell it apart from running them one at a time.

Checking "same result" directly would mean knowing what every transaction computes. The trick that databases (and exam papers) use instead looks only at the order of **conflicting** operations, and turns the question into "does this graph have a cycle?"

## What you'll use

**Two operations conflict** when they're from different transactions, on the same item, and at least one is a write:

| | `r2(A)` | `w2(A)` |
|---|---|---|
| `r1(A)` | no conflict | conflict |
| `w1(A)` | conflict | conflict |

Swapping two adjacent non-conflicting operations can't change anything. If you can swap your way from a schedule to a serial one, they're **conflict-equivalent**, and the schedule is **conflict serializable**.

**The precedence graph** does the swapping test in one go. Draw a node per transaction, and an edge Ti → Tj for every conflict where Ti's operation comes first.

```
r1(A) r2(B) w1(B) w2(A) r3(A)

r2(B) … w1(B)   →  T2 → T1
r1(A) … w2(A)   →  T1 → T2      a cycle: T1 → T2 → T1, so NOT conflict serializable
w2(A) … r3(A)   →  T2 → T3
```

- **No cycle**: conflict serializable. Every **topological order** of the graph (an order that respects every edge) is an equivalent serial schedule.
- **A cycle**: not conflict serializable. (It might still be *view* serializable; that's Day 70.)
- Commits and aborts aren't reads or writes, so they don't conflict.

## Steps

1. `starter/serial.py`: `conflicts`, `precedence_graph`, `has_cycle` (a depth-first search that notices when it comes back to a node it's still inside), `is_conflict_serializable`, `serial_orders` and `conflict_equivalent`.
2. `starter/answers.py`. Draw the graph on paper first.
3. `pytest phase-6-transactions-and-storage/day-069-as-if-one-at-a-time`

## The kata: How Many Are Safe?

A classic exam question: T1 = `r1(A) w1(A)` and T2 = `r2(A) w2(A)`. There are 6 ways to interleave them (keeping each transaction's own order). How many are conflict serializable? In `starter/serial.py`, write `count_serializable(t1, t2)` to answer it for any two transactions. `itertools.combinations(range(n), len(t1))` picks which positions T1's operations take.

## When you're stuck

- **`conflicts` reports `r1(A) r2(A)`**: two reads never conflict.
- **The graph is missing a transaction**: every transaction in the schedule is a key, even one with no edges (`3: []`).
- **`has_cycle` misses `{1: [1]}`**: a node pointing to itself is a cycle.
- **`has_cycle` says a diamond (1→2, 1→3, 2→4, 3→4) has a cycle**: reaching a node you've *finished* isn't a cycle; reaching one you're *still exploring* is. Track three states: new, visiting, done.
- **`serial_orders` gives orders for a cyclic graph**: no order can satisfy a cycle, so the list should be empty. Filter the permutations by every edge.
- **The kata counts 70 for two 4-step transactions**: that's every interleaving. Only those whose graph has no cycle count.
