# Day 68: Can We Undo It?

## The brief

Atomicity (Day 65) promises that an aborted transaction leaves no trace. Its own changes are easy: put the old values back. But what if someone else already *read* one of those values?

```
w1(A)  r2(A)  c2  a1
```

T1 changes A, T2 reads that change and **commits**, then T1 aborts. A has to go back to its old value, but T2 has already committed a result based on a value that never officially existed. Committed means permanent, so T2 can't be undone, and the database can't keep its promise. That schedule is **not recoverable**.

Today you sort schedules by how safely they can be undone. It's a favourite exam topic, and it's exactly why real databases hold write locks until commit (Day 71).

## What you'll use

**Reads-from**: Ti *reads from* Tj when Ti reads X and the last write of X before that was by Tj (Tj ≠ Ti). Writes undone by an abort don't count: after `w1(A) a1`, A is back to what it was before.

Three properties, each stricter than the last:

| Property | Rule | Why it matters |
|---|---|---|
| **Recoverable** | if Ti reads from Tj and Ti commits, Tj committed *before* Ti | an abort never has to undo a commit |
| **Cascadeless** (avoids cascading aborts, ACA) | Ti only reads values whose writer has already committed | one abort never drags others down |
| **Strict** | nobody reads *or writes* X while another transaction's write of X is uncommitted | undo is just "put back the old value" |

```
strict  ⊂  cascadeless  ⊂  recoverable  ⊂  all schedules
```

- `w1(A) r2(A) c1 c2` is recoverable (T1 commits first) but not cascadeless: if T1 had aborted, T2 would have had to abort too. That's a **cascading abort**.
- `w1(A) w2(A) c1 c2` is cascadeless (no reads at all) but not strict: T2 overwrote an uncommitted value. If T1 aborts, putting back "the value before T1" would wipe out T2's write.
- **Serial** schedules (one transaction at a time) are always strict.

**Cascading aborts** spread: if T1 aborts, everyone who read from T1 aborts, and everyone who read from *them*, and so on.

## Steps

`tools/coursekit/schedules.py` reads the notation for you: `parse("w1(A) r2(A) c1")`.

1. `starter/recovery.py`: `reads_from` first (everything else uses it), then `is_recoverable`, `is_cascadeless`, `is_strict`, and `cascade`.
2. `starter/answers.py`.
3. `pytest phase-6-transactions-and-storage/day-068-can-we-undo-it`

Do a few on paper first. For `w2(A) w1(B) r1(A) r2(B) c2 c1`: who reads from whom, and who commits first?

## The kata: Classify

In `starter/recovery.py`, write `classify(schedule)`: the strongest of `"strict"`, `"cascadeless"`, `"recoverable"`, or `"not recoverable"`. Since each property implies the next, check from the strongest down.

## When you're stuck

- **`reads_from` reports T1 reading from T1**: reading your own write doesn't count.
- **`w1(A) a1 r2(A)` says T2 reads from T1**: T1's write was undone by its abort. Remove an aborted transaction's writes from your "last writer" record.
- **`is_recoverable` fails `w1(A) r2(A)`** (nobody commits): the rule only applies to readers that *commit*. A reader that hasn't committed can still be aborted.
- **`is_strict` passes `w1(A) w2(A) c1 c2`**: strictness covers writes too, not just reads.
- **`cascade` misses T3 in `w1(A) r2(A) w2(A) r3(A)`**: it's transitive. Keep going until nothing new is added.
