# Checkpoint 2: Practice Test 2

This checkpoint sits between Day 52 and Day 53. It isn't one of the hundred days. Take it when you finish Phase 4, before MySQL gets advanced.

## The brief

Normalisation is the part of the databases syllabus GATE asks about most, and the part that slips away fastest. This 16-question paper covers Phase 4 only: functional dependencies, closure, keys, covers, decomposition, and 1NF to 4NF.

Set a timer for **45 minutes**, close your notes, and answer on paper first. Then type your answers into `starter/answers.py` and let the tests mark you. Aim for 20 of the 26 marks before moving on. If you get fewer, read [worked-examples.md](../worked-examples.md) in this phase and take the paper again a few days later.

## What you'll use

Days 41 to 51, and the question types from Day 39:

| Type | You answer | Marking in GATE |
|---|---|---|
| **MCQ** | one letter: `"B"` | a wrong answer loses 1/3 of its marks |
| **MSQ** | every correct letter, as a set: `{"A", "D"}` | all correct or nothing |
| **NAT** | a number: `12` | exact |

Unless a question says otherwise, the dependencies listed are all there are, apart from those they imply.

## Steps

Answer each question in `starter/answers.py`, then run:

```bash
pytest phase-4-normalisation/checkpoint-2-practice-test-2
```

Each passing test is a question right; marks are in brackets.

**Q1** (NAT, 1 mark). R(A, B, C, D) has A → B and B → C. How many attributes are in A⁺?

**Q2** (NAT, 2 marks). R(A, B, C, D, E) has A → B, BC → E and ED → A. How many candidate keys does R have?

**Q3** (MCQ, 1 mark). "If X → Y and X → Z, then X → YZ" is the:
(A) reflexivity rule  (B) augmentation rule  (C) union rule  (D) decomposition rule

**Q4** (MSQ, 2 marks). R(A, B, C, D) has A → B, B → C and C → A. Which dependencies hold?
(A) A → C  (B) BC → A  (C) A → BC  (D) D → A

**Q5** (NAT, 2 marks). How many dependencies are in a minimal cover of { A → BC, CD → E, B → D, E → A } (one attribute on each right side)?

**Q6** (MCQ, 2 marks). F = { A → B, B → C } and G = { A → B, B → C, A → C }. Which is true?
(A) F and G are equivalent  (B) F covers G, but G doesn't cover F  (C) G covers F, but F doesn't cover G  (D) neither covers the other

**Q7** (MCQ, 1 mark). R(A, B, C) with A → B is split into (A, B) and (A, C). The decomposition is:
(A) lossless and dependency-preserving  (B) lossless but not dependency-preserving  (C) lossy but dependency-preserving  (D) lossy and not dependency-preserving

**Q8** (MCQ, 2 marks). R(A, B, C, D) with AB → C, C → D and D → B is split into (A, B, C) and (C, D). The decomposition is:
(A) lossless and dependency-preserving  (B) lossless but not dependency-preserving  (C) lossy but dependency-preserving  (D) lossy and not dependency-preserving

**Q9** (NAT, 1 mark). R(A, B, C, D) has exactly one candidate key, {A}. How many superkeys does it have?

**Q10** (MCQ, 1 mark). Second normal form rules out:
(A) multivalued attributes  (B) a non-prime attribute depending on part of a candidate key  (C) a non-prime attribute depending on another non-prime attribute  (D) any dependency whose left side isn't a superkey

**Q11** (MCQ, 2 marks). R(A, B, C, D, E) has A → BCDE, BC → A and D → E. The highest normal form R is in is:
(A) 1NF  (B) 2NF  (C) 3NF  (D) BCNF

**Q12** (NAT, 2 marks). R(A, B, C, D) has A → B, B → C and C → D. How many relations does the 3NF synthesis algorithm produce?

**Q13** (NAT, 2 marks). R(A, B, C, D) has A → B and C → D. You decompose it into BCNF by splitting on each violating dependency in turn. How many relations do you end with?

**Q14** (MSQ, 2 marks). Which are true?
(A) every functional dependency is also a multivalued dependency  (B) if X →→ Y holds in R, so does X →→ R − X − Y  (C) every relation in 4NF is in BCNF  (D) every relation in BCNF is in 4NF

**Q15** (MCQ, 1 mark). A shop adds a `county_totals` table holding each county's total sales, kept next to the normalised `sales` table. The trade-off is:
(A) faster reads, but the totals drift unless every write also updates them  (B) it removes update anomalies  (C) it needs no extra storage  (D) it puts the schema in BCNF

**Q16** (NAT, 2 marks). R(A, B, C, D) has A → B, B → C, C → D and D → A. How many candidate keys does it have?

## When you're stuck

Don't look now. After marking, here's where to look again:

- Q1, Q2, Q9, Q16: Day 43 (closure and keys). Q3, Q4, Q6: Day 44. Q5: Day 45.
- Q7, Q8: Days 46 and 47. Q10, Q11: Days 48 and 49. Q12, Q13: Day 49. Q14: Day 50. Q15: Day 51.
- [worked-examples.md](../worked-examples.md) walks through questions like these step by step.
- **A question marked wrong that you're sure of**: check the answer's form. MCQ is a string like `"B"`; MSQ is a *set* of strings; NAT is an `int`.
