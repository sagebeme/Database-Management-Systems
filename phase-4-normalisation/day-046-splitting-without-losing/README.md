# Day 46: Splitting Without Losing

## The brief

Normalising means splitting tables. But a split can go wrong in a sneaky way. The college's `enrolments(student, course, lecturer)` table gets split into "which lecturer does each student have?" and "which lecturer teaches each course?". Both look sensible. Join them back, and Achieng is suddenly enrolled in Compilers, a course she never took, because Dr Otieno teaches both Databases and Compilers.

A split that can't be joined back to exactly the original rows is **lossy**. The name is misleading: you don't lose rows, you **gain** wrong ones (*spurious* tuples), and lose the information about which rows were real. Today: a one-line test for splitting in two, and the chase algorithm for splitting into any number of parts.

## What you'll use

**A decomposition** of R into R₁, ..., Rₙ is **lossless** if, for every legal instance r, joining the projections gives back exactly r:

π<sub>R₁</sub>(r) ⋈ ... ⋈ π<sub>Rₙ</sub>(r) = r

(The join always contains r; the danger is extra rows.)

**Two parts: the binary test.** R₁, R₂ is lossless **if and only if** the common attributes are a superkey of at least one part:

(R₁ ∩ R₂)⁺ ⊇ R₁  **or**  (R₁ ∩ R₂)⁺ ⊇ R₂

With F = {course → lecturer}:

- `(student, lecturer)` + `(course, lecturer)`: common = {lecturer}, and lecturer⁺ = {lecturer}. Lossy.
- `(student, course)` + `(course, lecturer)`: common = {course}, and course⁺ ⊇ {course, lecturer}. Lossless.

**Any number of parts: the chase.** Draw a table with a row per part and a column per attribute. Put `a` where the part has the attribute, and a unique `b` everywhere else. Then apply each FD X → Y: rows that agree on X must agree on Y, so overwrite their Y values to match, preferring `a`. Repeat until nothing changes. If any row becomes all `a`, the split is lossless.

```
R(A,B,C,D), parts AB, BC, CD, F = {A→B, B→C, C→D, D→A}
        A    B    C    D
AB      a    a    b13  b14       B→C: rows AB, BC agree on B (a), so C becomes a in AB
BC      b21  a    a    b24       C→D: rows AB, BC, CD now agree on C, so D becomes a
CD      b31  b32  a    a         row AB is now  a a a a :  lossless
```

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS split;"
tools/mysql.sh split < phase-4-normalisation/day-046-splitting-without-losing/setup.sql
```

1. `starter/lossless.py`, `binary_lossless`.
2. `chase`: the tableau algorithm. Represent each row as a dict from attribute to symbol.
3. `starter/0-split_badly.sql`: `student_lecturer` and `course_lecturer`, built with `CREATE TABLE ... AS SELECT DISTINCT`.
4. `starter/1-ghost_rows.sql`: join them back and list the rows that were never in `enrolments`.
5. `starter/2-split_well.sql` and `starter/3-rejoin.sql`: the lossless split, and the join that proves it. Drop the first split's tables before trying the second at your prompt.
6. `starter/answers.py`.
7. `pytest phase-4-normalisation/day-046-splitting-without-losing`

## The kata: Count the Ghosts

In `starter/lossless.py`, write `spurious(rows, parts)`: project real rows onto each part, join them back in Python, and return the ghost rows. This checks one instance; the chase checks every possible instance.

## When you're stuck

- **`binary_lossless` says yes to AB + CD**: the common attributes are empty, and the closure of nothing is nothing. That's lossy: it's a product.
- **`chase` never finishes**: only set `changed = True` when you actually overwrite a value.
- **`chase` gets the textbook example wrong**: when you equate two symbols, change *every* row that holds the old symbol in that column, not just the rows in the group.
- **`1-ghost_rows.sql` lists every row**: the `NOT EXISTS` must compare all three columns with `enrolments`.
- **`Table 'course_lecturer' already exists`** at your prompt: both splits make `course_lecturer`. Drop it between tries.
