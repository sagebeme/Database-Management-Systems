# Checkpoint 3: Practice Test 3

This checkpoint sits between Day 78 and Day 79. It isn't one of the hundred days. Take it when you finish Phase 6, before leaving MySQL behind.

## The brief

Phase 6 is the most GATE-heavy phase of the course: schedules, serializability, locking, timestamps, recovery, file organisation and B+ trees. This 16-question paper covers all of it.

Set a timer for **45 minutes**, close your notes, and answer on paper first. Then type your answers into `starter/answers.py` and let the tests mark you. Aim for 21 of the 27 marks. If you get fewer, read [worked-examples.md](../worked-examples.md) in this phase and take the paper again a few days later.

## What you'll use

Days 65 to 77, and the question types from Day 39:

| Type | You answer | Marking in GATE |
|---|---|---|
| **MCQ** | one letter: `"B"` | a wrong answer loses 1/3 of its marks |
| **MSQ** | every correct letter, as a set: `{"A", "D"}` | all correct or nothing |
| **NAT** | a number: `12` | exact |

Schedules use the course notation: `r1(A)` is T1 reading A, `w2(B)` is T2 writing B, `c1` is T1 committing.

## Steps

Answer each question in `starter/answers.py`, then run:

```bash
pytest phase-6-transactions-and-storage/checkpoint-3-practice-test-3
```

**Q1** (MCQ, 1 mark). Undoing an unfinished transaction's writes after a crash protects which property?
(A) atomicity  (B) consistency  (C) isolation  (D) durability

**Q2** (MCQ, 1 mark). A dirty read is when:
(A) T2 reads a value T1 wrote before T1 commits  (B) T2 reads the same item twice and gets two values  (C) a query run twice returns new rows the second time  (D) two transactions write the same item and one write is lost

**Q3** (MCQ, 2 marks). The schedule `r1(A) w1(A) r2(A) c1 w2(A) c2` is:
(A) strict  (B) cascadeless but not strict  (C) recoverable but not cascadeless  (D) not recoverable

**Q4** (NAT, 2 marks). How many edges does the precedence graph of `r1(X) r2(Y) w3(X) r2(X) w1(Y)` have?

**Q5** (MCQ, 2 marks). The schedule `r1(A) w1(A) r2(A) w2(A) r1(B) w1(B) r2(B) w2(B)` is:
(A) not conflict serializable  (B) conflict serializable, equivalent to T1 then T2  (C) conflict serializable, equivalent to T2 then T1  (D) conflict equivalent to both serial orders

**Q6** (NAT, 2 marks). How many serial schedules is `w1(A) r2(A) w1(B) r3(B)` conflict equivalent to?

**Q7** (MCQ, 2 marks). The schedule `r1(A) w2(A) w1(A) w3(A)` is:
(A) conflict serializable  (B) view serializable but not conflict serializable  (C) neither view nor conflict serializable  (D) serial

**Q8** (MSQ, 2 marks). Which are true?
(A) strict two-phase locking prevents cascading rollbacks  (B) basic two-phase locking prevents deadlocks  (C) conservative two-phase locking prevents deadlocks  (D) rigorous two-phase locking holds every lock until the transaction ends

**Q9** (MCQ, 1 mark). Under the Thomas write rule, when T writes X, TS(T) < W-timestamp(X), and R-timestamp(X) ≤ TS(T):
(A) T is rolled back  (B) the write is ignored and T carries on  (C) T waits  (D) the newer write is undone

**Q10** (MCQ, 2 marks). Under basic timestamp ordering, TS(T1) = 10. X has R-timestamp 15 and W-timestamp 8. T1 asks to write X. What happens?
(A) the write goes ahead  (B) the write is ignored  (C) T1 is rolled back  (D) T1 waits for the reader

**Q11** (NAT, 2 marks). The log reads, oldest first, then the system crashes:

```
<T1 start> <T1, X, 100, 50> <T2 start> <T2, Y, 200, 250> <T2 commit>
<T3 start> <T3, X, 50, 70> <T1, Z, 5, 6>
```

Each update is `<transaction, item, old value, new value>`. After undo/redo recovery, what is X + Y + Z?

**Q12** (NAT, 2 marks). A file of 50,000 records of 200 bytes, sorted on its key, is stored unspanned in 1,024-byte blocks. A primary (sparse) index has one 16-byte entry per data block, also in 1,024-byte blocks. How many block reads does it take to find a record by key, with binary search on the index?

**Q13** (NAT, 2 marks). A B+ tree leaf is a 512-byte block holding keys of 9 bytes, a 7-byte record pointer per key, and one 6-byte pointer to the next leaf. What is the most keys a leaf can hold?

**Q14** (NAT, 1 mark). A B-tree node has at most 4 children (so at most 3 keys). What is the most keys a B-tree with 3 levels can hold?

**Q15** (MCQ, 1 mark). In MySQL's InnoDB, the leaf entries of a secondary index hold:
(A) the whole row  (B) the row's primary key value  (C) the row's physical disk address  (D) nothing but the indexed column

**Q16** (MSQ, 2 marks). Which are true?
(A) wait-die and wound-wait both avoid starvation if a restarted transaction keeps its original timestamp
(B) in wait-die, an older transaction may wait for a younger one
(C) in wound-wait, a younger transaction may wait for an older one
(D) in wait-die, a younger transaction asking for a lock held by an older one waits

## When you're stuck

Don't look now. After marking, here's where to look again:

- Q1, Q2: Days 65 and 66. Q3: Day 68. Q4–Q6: Day 69. Q7: Day 70.
- Q8: Day 71. Q9, Q10, Q16: Day 72. Q11: Day 73.
- Q12: Day 74. Q13, Q14: Days 75 and 76. Q15: Day 77.
- [worked-examples.md](../worked-examples.md) walks through questions like these step by step.
- **A question marked wrong that you're sure of**: check the answer's form. MCQ is a string like `"B"`; MSQ is a *set* of strings; NAT is an `int`.
