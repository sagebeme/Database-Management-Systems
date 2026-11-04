# Day 99: The Final Exam

## The brief

Ninety-eight days ago you didn't know what a table was. This is the whole subject in one sitting: a 30-question paper in the style of GATE's Databases section, covering everything from `NULL`s to B+ trees to backups.

Set a timer for **90 minutes**, close your notes, and answer on paper first. Then type your answers into `starter/answers.py` and let the tests mark you. Aim for 35 of the 46 marks. Below that, the list at the bottom says which days to go back to, and that's what tomorrow's capstone is for anyway: it will make you use all of it.

## What you'll use

Everything from Days 1 to 98, and the GATE question types from Day 39:

| Type | You answer | Marking in GATE |
|---|---|---|
| **MCQ** (multiple choice) | exactly one letter: `"B"` | a wrong answer loses 1/3 of its marks |
| **MSQ** (multiple select) | every correct letter, as a set: `{"A", "D"}` | all correct or nothing |
| **NAT** (numerical answer) | a number: `12` | exact |

## Steps

Answer each question in `starter/answers.py`, then run `pytest phase-8-expert/day-099-the-final-exam`. Each passing test is a question right; marks are in brackets. The paper is out of 46.

### SQL

**Q1** (NAT, 1 mark). Column `a` of table `T` holds `3, NULL, 5, 5, NULL`. What does `SELECT COUNT(DISTINCT a) + COUNT(*) FROM T;` return?

**Q2** (NAT, 1 mark). Column `a` holds `1, 2, NULL`. How many rows does `SELECT * FROM T WHERE NOT (a = 1);` return?

**Q3** (NAT, 2 marks). `sales(shop, amount)` holds `('A', 10), ('A', 20), ('B', 5), ('B', NULL), ('C', NULL)`. How many rows does this return?

```sql
SELECT shop FROM sales GROUP BY shop HAVING SUM(amount) > 6 OR SUM(amount) IS NULL;
```

**Q4** (NAT, 1 mark). Scores are `90, 85, 85, 80`. For the row with 80, what is `rank() OVER (ORDER BY score DESC)` plus `dense_rank() OVER (ORDER BY score DESC)`?

**Q5** (NAT, 2 marks). `R(a)` holds `1, 1, 2, NULL`; `S(a)` holds `1, 2, 2, NULL`. How many rows does `SELECT * FROM R LEFT JOIN S ON R.a = S.a;` return?

### Design

**Q6** (NAT, 2 marks). Entity A has a multivalued attribute. B is a weak entity owned by A. C is a strong entity. A and C are related many-to-many, and the relationship has an attribute of its own. What is the fewest tables that can represent this?

**Q7** (NAT, 1 mark). R(A, B) = {(1, x), (1, y), (1, z), (2, x), (2, y), (3, x), (3, y), (3, z), (4, z)} and S(B) = {(x), (z)}. How many tuples are in R ÷ S?

**Q8** (NAT, 2 marks). R(A, B, C, D, E, F) has the dependencies AB → C, C → D, D → A, E → F. How many candidate keys does R have?

**Q9** (MCQ, 1 mark). R(A, B, C, D) has AB → C and C → D, and no other dependencies except those they imply. The highest normal form R is in is:
(A) 1NF  (B) 2NF  (C) 3NF  (D) BCNF

**Q10** (MCQ, 2 marks). R(A, B, C) has AB → C and C → B. The highest normal form R is in is:
(A) 1NF  (B) 2NF  (C) 3NF  (D) BCNF

**Q11** (NAT, 2 marks). How many dependencies are in a minimal cover of { A → BC, B → C, A → B, AB → C }?

**Q12** (MSQ, 2 marks). R(A, B, C, D) has A → B and C → D. Which decompositions are both lossless and dependency-preserving?
(A) {AB, CD}  (B) {AB, ACD}  (C) {ABC, CD}  (D) {AB, BCD}

**Q13** (MSQ, 1 mark). Which are always true?
(A) every relation in BCNF is in 3NF  (B) every relation with exactly two attributes is in BCNF  (C) a lossless, dependency-preserving decomposition into 3NF exists  (D) a lossless, dependency-preserving decomposition into BCNF exists

### Transactions

**Q14** (NAT, 2 marks). How many edges does the precedence graph of this schedule have?
`r1(A) r2(B) w2(A) r3(A) w1(B) w3(B)`

**Q15** (MCQ, 1 mark). The schedule `w1(A) r2(A) w2(B) c2 c1` is:
(A) strict  (B) cascadeless but not strict  (C) recoverable but not cascadeless  (D) not recoverable

**Q16** (NAT, 1 mark). T1 has 3 operations and T2 has 2. How many different schedules (interleavings that keep each transaction's own order) of T1 and T2 are there?

**Q17** (MCQ, 1 mark). Basic two-phase locking guarantees:
(A) no deadlocks  (B) conflict serializability  (C) cascadeless schedules  (D) none of these

**Q18** (MSQ, 2 marks). T1 has timestamp 5 and T2 has timestamp 10 (T1 is older). Which are true?
(A) under wait-die, if T2 asks for a lock T1 holds, T2 is rolled back
(B) under wound-wait, if T2 asks for a lock T1 holds, T2 waits
(C) under wait-die, if T1 asks for a lock T2 holds, T1 waits
(D) under wound-wait, if T1 asks for a lock T2 holds, T1 is rolled back

**Q19** (NAT, 2 marks). The log reads, oldest first, then the system crashes:

```
<T1 start> <T1, A, 10, 20> <T2 start> <T2, B, 5, 15> <T1 commit>
<checkpoint {T2}> <T3 start> <T3, C, 1, 2> <T2, B, 15, 25> <T3 commit>
```

Each update record is `<transaction, item, old value, new value>`. After undo/redo recovery, what is the value of B?

### Storage and indexes

**Q20** (NAT, 2 marks). A sorted file holds 1,000,000 records of 100 bytes in 4,096-byte blocks, unspanned. How many block reads does a binary search need in the worst case?

**Q21** (NAT, 2 marks). B+ tree blocks are 1,024 bytes, keys 10 bytes and block pointers 8 bytes. What is the most child pointers an internal node can hold?

**Q22** (NAT, 2 marks). A B+ tree's leaves hold at most 50 keys and its internal nodes at most 100 children. With 1,000,000 keys and every node full, how many levels does the tree have, counting the leaves?

**Q23** (MCQ, 1 mark). A table can have:
(A) any number of clustering indexes  (B) at most one clustering index  (C) no secondary index once it has a clustering index  (D) a clustering index only on its primary key

**Q24** (NAT, 2 marks). R has 1,000 blocks and S has 500. A block nested-loop join uses the smaller relation as the outer and has 52 buffer blocks: one for the inner relation, one for the output, the rest for the outer. How many block reads does it take?

### Beyond one server

**Q25** (NAT, 1 mark). Keys 0 to 19 are spread over servers with `key mod N`. When N goes from 4 to 5, what percentage of the keys move to a different server?

**Q26** (MCQ, 2 marks). In PostgreSQL, which anomaly can still happen at `REPEATABLE READ`?
(A) dirty read  (B) non-repeatable read  (C) phantom read  (D) write skew

**Q27** (MSQ, 2 marks). Which are true?
(A) a star schema's fact table holds measurements and foreign keys to its dimensions
(B) the dimensions of a star schema are normally kept in 3NF
(C) a type 2 slowly changing dimension adds a row when a described thing changes
(D) `GROUP BY ROLLUP (a, b)` includes a subtotal for every value of `b` across all `a`

**Q28** (NAT, 1 mark). A database is dumped with `pg_dump` every night at 01:00 and there's no WAL archiving. The disk dies at 20:00. How many hours of writes are lost?

**Q29** (MCQ, 1 mark). In PostgreSQL, which makes row-level security policies apply to the table's owner too?
(A) `ALTER TABLE t ENABLE ROW LEVEL SECURITY`  (B) `ALTER TABLE t FORCE ROW LEVEL SECURITY`  (C) `REVOKE ALL ON t FROM owner`  (D) `CREATE POLICY p ON t TO owner`

**Q30** (NAT, 1 mark). In Redis: `SET k 5`, `INCR k`, `INCRBY k 10`, `DECR k`. What does `GET k` return?

## The kata: Mark It Like GATE

Real GATE takes marks off for wrong MCQs. In `starter/marking.py`, write `gate_score(paper, given)`: a right answer earns its marks, a wrong MCQ loses a third of its marks, and a wrong MSQ or NAT answer or a blank costs nothing. Return a `Fraction`, because thirds don't fit exactly in a float. Then mark your own first attempt at this paper with it: did guessing pay?

## When you're stuck

Don't look now. After marking, here's where to look again:

- Q1–Q5: Days 8, 11, 20, 54 (`COUNT`, `NULL`s, outer joins, ranking).
- Q6, Q7: Days 33, 34, 37.
- Q8–Q13: Days 43, 45, 46, 47, 48, 49.
- Q14–Q19: Days 68, 69, 71, 72, 73.
- Q20–Q24: Days 74, 76, 77, 91.
- Q25: Day 92. Q26: Day 67. Q27: Day 95. Q28: Day 93. Q29: Day 94. Q30: Day 87.
- **A question marked wrong that you're sure of**: check the answer's form. MCQ is a string like `"B"`; MSQ is a *set* of strings; NAT is an `int`.
