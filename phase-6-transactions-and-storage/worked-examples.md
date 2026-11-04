# Phase 6: worked examples

Nine exam-style problems with the working shown step by step. They sit outside the hundred days. Read them after Day 77 and before [Checkpoint 3](checkpoint-3-practice-test-3/README.md). Cover the working, try each one yourself, then compare.

Notation: `r1(A)` is T1 reading A, `w2(B)` is T2 writing B, `c1` is T1 committing.

---

## 1. Recoverable, cascadeless, strict

Classify each schedule. Ask three questions in order:

1. **Recoverable**: if Tj reads something Ti wrote, does Ti commit before Tj does?
2. **Cascadeless**: does every read see only *committed* data?
3. **Strict**: are reads *and overwrites* of an item held back until its last writer commits?

| Schedule | Working | Answer |
|---|---|---|
| `w1(A) r2(A) c2 c1` | T2 read T1's A and committed first. If T1 aborts now, T2 can't be undone. | **not recoverable** |
| `w1(A) r2(A) c1 c2` | T2 read uncommitted data, but T1 committed first. | **recoverable**, not cascadeless |
| `w1(A) w2(A) c1 c2` | Nobody reads uncommitted data, but T2 overwrote T1's uncommitted A. | **cascadeless**, not strict |
| `w1(A) c1 r2(A) w2(A) c2` | T2 touches A only after T1 commits. | **strict** |

Each class sits inside the one before: strict ⊂ cascadeless ⊂ recoverable.

---

## 2. Precedence graphs and equivalent serial orders

`r1(A) w2(A) r1(B) w3(B) r4(C)`. Draw an edge Ti → Tj for each pair of operations from different transactions, on the same item, at least one a write, with Ti's first:

- r1(A) then w2(A): **T1 → T2**.
- r1(B) then w3(B): **T1 → T3**.
- T4 touches only C, which nobody else touches: no edges.

No cycle, so it's **conflict serializable**. The equivalent serial schedules are the orders that respect every edge (the *topological orders*). Of the 4! = 24 orders of four transactions, T1 must come before both T2 and T3, which holds in a third of them, and T4 can go anywhere.

**24 / 3 = 8 serial orders.** "How many serial schedules is it equivalent to?" means counting topological orders, not edges.

---

## 3. View serializable but not conflict serializable

`r2(B) w1(B) w2(B) w3(B)`.

**Conflict**: r2(B) before w1(B) gives T2 → T1; w1(B) before w2(B) gives T1 → T2. That's a cycle, so it's **not conflict serializable**.

**View**: compare it with the serial schedule T2 T1 T3, checking the three view conditions:

- **Initial reads**: T2 reads B's original value in both. ✓
- **Who reads from whom**: no other reads. ✓
- **Final write**: T3 writes B last in both. ✓

So it's **view serializable**. The giveaway is the **blind writes**: T1 and T3 write B without reading it, and T3's final write makes the earlier ones invisible. A schedule that's view but not conflict serializable always has a blind write.

---

## 4. Could two-phase locking produce this schedule?

`r1(A) w2(A) w2(B) r1(B)`.

Under 2PL, each transaction locks everything it needs before it unlocks anything:

- T2 writes A after T1 read it, so **T1 must release A before w2(A)**.
- T1 reads B after T2 wrote it, so T1 can only lock B after T2 lets go of it. T1 can't take a shared lock on B early either, because T2 needs an exclusive one.
- So T1 locks B *after* releasing A. That breaks two-phase locking.

**No.** The fast route: the precedence graph has T1 → T2 (on A) and T2 → T1 (on B), a cycle. 2PL only ever produces conflict serializable schedules, so a cycle rules it out straight away.

---

## 5. Timestamp ordering, with and without Thomas

TS(T1) = 10, TS(T2) = 20, TS(T3) = 30. Every item starts with read and write timestamps of 0. Run `r1(X) w2(X) w1(X) r3(X) w1(Y) r2(Y)`:

| Operation | Check | Basic TO | Thomas write rule |
|---|---|---|---|
| r1(X) | 10 ≥ W-TS(X) = 0 | ok, R-TS(X) = 10 | ok |
| w2(X) | 20 ≥ R-TS 10 and W-TS 0 | ok, W-TS(X) = 20 | ok |
| w1(X) | 10 ≥ R-TS 10, but 10 < W-TS 20 | **T1 rolled back** | **write ignored**: T2's newer value stands |
| r3(X) | 30 ≥ W-TS 20 | ok | ok |
| w1(Y) | | skipped: T1 is gone | ok, W-TS(Y) = 10 |
| r2(Y) | 20 ≥ W-TS(Y) | ok | ok |

The rules for T writing X: if TS(T) < R-TS(X), a younger transaction already read X, so **T is always rolled back**. If TS(T) < W-TS(X) only, basic TO rolls T back, but Thomas **ignores the write**, because nobody will ever read it.

---

## 6. Wait-die and wound-wait

T1 is older (TS 10) and T2 is younger (TS 20).

| Who asks for a lock the other holds | Wait-die | Wound-wait |
|---|---|---|
| **T1** (older) asks | T1 **waits** | T1 **wounds** T2: T2 is rolled back |
| **T2** (younger) asks | T2 **dies**: rolled back | T2 **waits** |

To remember them: in both schemes, only the **older** transaction is ever allowed to wait in wait-die, and only the **younger** in wound-wait. In both, the one rolled back is always the younger. A restarted transaction keeps its original timestamp, so it eventually becomes the oldest and can't starve.

---

## 7. Undo/redo recovery with a checkpoint

The log, oldest first, then a crash. Updates are `<transaction, item, old, new>`:

```
<T1 start>  <T1, A, 100, 80>  <T2 start>  <T2, B, 50, 60>  <T1 commit>
<checkpoint {T2}>
<T3 start>  <T3, A, 80, 95>  <T2, C, 7, 9>  <T3 commit>
```

1. **Who committed?** T1 and T3. **Losers**: T2 (started, never committed).
2. **Undo the losers, backwards**: C goes back to 7, then B goes back to 50. T2 started *before* the checkpoint, so the undo pass has to read back past it to T2's first update.
3. **Redo the winners, forwards from the checkpoint**: T3's A = 95. T1 committed before the checkpoint, so its writes are already on disk and need no redo.

**After recovery: A = 95, B = 50, C = 7**, whatever was on disk at the crash. The checkpoint saves redo work; it doesn't shorten the undo pass for a transaction that was still running.

---

## 8. Blocks, indexes and reads

40,000 records of 120 bytes, sorted on the key, unspanned in 2,048-byte blocks. Index entries are 20 bytes (a 12-byte key and an 8-byte block pointer).

| Question | Working | Answer |
|---|---|---|
| Blocking factor | ⌊2048 / 120⌋ | **17** records per block |
| Data blocks | ⌈40000 / 17⌉ | **2,353** |
| Binary search on the data file | ⌈log₂ 2353⌉ | **12** reads |
| Index entries per block (fan-out) | ⌊2048 / 20⌋ | **102** |
| Primary (sparse) index: one entry per data block | ⌈2353 / 102⌉ = 24 blocks; ⌈log₂ 24⌉ + 1 | **6** reads |
| Secondary (dense) index: one entry per record | ⌈40000 / 102⌉ = 393 blocks; ⌈log₂ 393⌉ + 1 | **10** reads |
| Multilevel primary index | level 1: 24 blocks; level 2: ⌈24 / 102⌉ = 1 block; 2 levels + 1 | **3** reads |

The "+1" is always the data block itself. Floors for "how many fit", ceilings for "how many blocks".

---

## 9. B+ tree order, then inserting

**Order from block size.** 2,048-byte blocks, 12-byte keys, 8-byte block pointers, 10-byte record pointers.

- **Internal node** with p children: p pointers and p − 1 keys, so 8p + 12(p − 1) ≤ 2048, 20p ≤ 2060, **p = 103**.
- **Leaf** with n keys: n (key, record pointer) pairs plus one next-leaf pointer, so 22n + 8 ≤ 2048, **n = 92**.

**Inserting.** A B+ tree of order 4 (at most 3 keys per node), inserting 10, 20, 30, 40, 50, 60, 70, splitting as on Day 76:

| Insert | Tree afterwards |
|---|---|
| 10, 20, 30 | `[10 20 30]` (one leaf, also the root) |
| 40 | the leaf would have 4 keys, so split it: `[10 20]` `[30 40]`, and **copy** 30 up into a new root `[30]` |
| 50 | `[30]` over `[10 20]` `[30 40 50]` |
| 60 | the right leaf splits into `[30 40]` `[50 60]`, and 50 is copied up: root `[30 50]` |
| 70 | `[30 50]` over `[10 20]` `[30 40]` `[50 60 70]` |

Inserting keys in increasing order leaves every leaf except the last half full. That's why bulk loading (the Day 76 kata) builds trees from sorted data instead.

**Check the convention.** Exam questions say how to split: which half gets the extra key, and whether "order" counts keys or children. Read that line twice before drawing anything.
