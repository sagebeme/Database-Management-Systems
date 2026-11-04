# Day 70: View Serializability

## The brief

Yesterday's test, "no cycle in the precedence graph", is safe but fussy. Look at this schedule:

```
r1(A)  w2(A)  w1(A)  w3(A)
```

The graph has T1 → T2 (r1 before w2) and T2 → T1 (w2 before w1): a cycle, so it's **not** conflict serializable. Yet it gives exactly the same result as running T1, then T2, then T3. T1 reads the original A, and whatever T1 and T2 write, T3 overwrites it at the end. T2's write is never read by anyone; it's a **blind write**, written without reading.

**View serializability** captures this. Two schedules are equivalent when every transaction *sees* the same values, and the database ends up with the same final values, whatever order the overwritten writes happened in.

## What you'll use

Schedules S and S' are **view-equivalent** when:

1. **Same reads from the start**: if Ti reads the initial value of A in S, it does in S' too.
2. **Same reads-from**: if Ti reads the A that Tj wrote in S, it does in S' too.
3. **Same final writes**: whoever writes A last in S writes it last in S'.

A schedule is **view serializable** if it's view-equivalent to *some* serial schedule.

```
every conflict serializable schedule  ⊂  view serializable  ⊂  all schedules
```

- A view-serializable schedule that isn't conflict serializable always has a **blind write**.
- **There's no cheap test.** For conflict serializability you look for a cycle, which is fast. For view serializability, the problem is NP-complete in general. You can do no better than try serial orders, which is fine for exam-sized schedules and hopeless for a real database. That's why real systems use conflict-based methods (locks, Day 71) and accept that they refuse some schedules that would have been fine.

## Steps

1. `starter/view.py`: `reads`, `final_writes`, `view_equivalent`, `is_view_serializable` (try every order of the transactions) and `blind_writes`. `conflict_serializable` is done for you.
2. `starter/answers.py`.
3. `pytest phase-6-transactions-and-storage/day-070-view-serializability`

Try `r1(A) w2(A) w1(A) w3(A)` on paper: who reads what, who writes A last, and which serial order matches?

## The kata: Explain It

In `starter/view.py`, write `explain(schedule)`: `"conflict serializable"`, `"view serializable only"`, or `"not serializable"`. Use the cheap test first.

## When you're stuck

- **`reads` loses a read that happens twice**: it's a `Counter`, so add 1 each time (`found[key] += 1`).
- **Reading the initial value shows up with a writer**: if nobody has written the item yet, the writer is `None`.
- **`is_view_serializable` builds serial schedules with commits in them**: keep only the reads and writes, each transaction's in its own order.
- **`view_equivalent` says two schedules with different operations are equivalent**: check the operations match first, as a multiset of (kind, txn, item).
- **`blind_writes` repeats `(1, 'A')`**: each (transaction, item) once.
