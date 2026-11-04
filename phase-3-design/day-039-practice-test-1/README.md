# Day 39: Practice Test 1

## The brief

Halfway through the design phase, it's time to check what has stuck. This is a 16-question paper in the style of GATE's Databases section, covering Phases 1 to 3: SQL and `NULL`s, joins, keys, ER diagrams and mapping, relational algebra and calculus.

Set a timer for **45 minutes**, close your notes, and answer on paper first. Then type your answers into `starter/answers.py` and let the tests mark you. Only look things up *after* you've marked yourself.

## What you'll use

Everything from Days 1 to 38, and the GATE question types:

| Type | You answer | Marking in GATE |
|---|---|---|
| **MCQ** (multiple choice) | exactly one letter: `"B"` | +1 or +2; a wrong answer loses 1/3 of its marks |
| **MSQ** (multiple select) | every correct letter, as a set: `{"A", "D"}` | all correct or nothing; no negative marks |
| **NAT** (numerical answer) | a number: `12` | exact; no negative marks |

So in real GATE, guess on MSQ and NAT, but think twice before guessing an MCQ.

## Steps

Answer each question in `starter/answers.py`, then run `pytest phase-3-design/day-039-practice-test-1`. Each passing test is a question right; the marks are in brackets. The paper is out of 23.

**Q1** (NAT, 1 mark). Table `T` has one column `a` holding `1, 2, NULL, 4, NULL`. What does `SELECT COUNT(*) - COUNT(a) FROM T;` return?

**Q2** (NAT, 1 mark). Column `b` holds `2, NULL, 4`. What does `SELECT AVG(b) FROM U;` return?

**Q3** (MCQ, 1 mark). `R` has rows; column `S.y` contains at least one `NULL`. What does `SELECT * FROM R WHERE x NOT IN (SELECT y FROM S);` return?
(A) every row of R  (B) no rows  (C) the rows of R where x is NULL  (D) an error

**Q4** (NAT, 1 mark). `R` has 4 rows and `S` has 3, no `NULL`s. What is the **largest** number of rows `SELECT * FROM R JOIN S ON R.k = S.k;` can return?

**Q5** (NAT, 2 marks). R(A, B, C, D, E) has exactly two candidate keys, {A, B} and {C}. How many superkeys does R have?

**Q6** (MCQ, 1 mark). The primary key of a weak entity's table is:
(A) its partial key  (B) its owner's primary key plus its partial key  (C) its owner's primary key alone  (D) a surrogate key it generates

**Q7** (NAT, 2 marks). An ER diagram has entities E1, E2 and E3. E1 has one multivalued attribute. E1–E2 is M:N and E2–E3 is 1:N, both with partial participation. What is the fewest tables that can represent it?

**Q8** (NAT, 1 mark). R and S are union-compatible, |R| = 8, |S| = 5 and |R ∩ S| = 3. What is |R ∪ S|?

**Q9** (NAT, 2 marks). R(A, B) = {(1, x), (1, y), (2, x), (3, y), (3, x)} and S(B) = {(x), (y)}. How many tuples does R ÷ S have?

**Q10** (MCQ, 1 mark). Which SQL computes π<sub>A</sub>(σ<sub>B=1</sub>(R)) exactly?
(A) `SELECT A FROM R WHERE B = 1`  (B) `SELECT DISTINCT A FROM R WHERE B = 1`  (C) `SELECT DISTINCT A FROM R GROUP BY B`  (D) `SELECT A FROM R HAVING B = 1`

**Q11** (MSQ, 2 marks). Which are basic (fundamental) relational algebra operators?
(A) select  (B) natural join  (C) set difference  (D) intersection  (E) rename

**Q12** (MCQ, 1 mark). The tuple calculus query { t | ¬(t ∈ R) } is:
(A) safe, and always empty  (B) unsafe  (C) equivalent to R  (D) equivalent to R − R

**Q13** (NAT, 2 marks). A relation has two attributes, with domains of 3 and 2 values. How many different relation instances are possible (the empty one included)?

**Q14** (NAT, 2 marks). R(A, B, C) has 100 tuples and S(C, D) has 50. C is the primary key of S, and R.C is a `NOT NULL` foreign key referencing S. How many tuples does R ⋈ S have?

**Q15** (MCQ, 1 mark). A child table's foreign key says `ON DELETE SET NULL`. When a parent row is deleted:
(A) its children are deleted  (B) the delete is refused  (C) its children's foreign key becomes NULL  (D) the parent's key becomes NULL

**Q16** (MSQ, 2 marks). Which are true of views in MySQL?
(A) a view stores its own copy of the rows  (B) a view over one table, without aggregates or `DISTINCT`, can accept `UPDATE`s  (C) `WITH CHECK OPTION` refuses writes that would produce rows the view can't see  (D) dropping a view drops its base tables

## When you're stuck

Don't look now. After marking, here's where to look again:

- Q1–Q3: Days 8, 11, 22 (`COUNT`, `NULL`s, the `NOT IN` trap).
- Q4, Q14: Days 19, 23, 37 (join sizes: a foreign key to a key matches exactly once).
- Q5: Day 30. Q6, Q7: Days 33, 34.
- Q8–Q13: Days 35–38.
- Q15: Day 31. Q16: Day 26.
- **A question marked wrong that you're sure of**: check the answer's form. MCQ is a string like `"B"`; MSQ is a *set* of strings; NAT is an `int`.
