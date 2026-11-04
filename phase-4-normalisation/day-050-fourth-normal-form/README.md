# Day 50: Fourth Normal Form

## The brief

The tuition centre's `tutor_offers` table lists each tutor, a subject they teach and a language they teach in. Achieng teaches Maths and Physics, in English, Kiswahili and Dholuo, so she needs **six** rows: every subject paired with every language. The key is all three columns. There are no FDs at all, so the table is in BCNF, and yet:

- When Achieng starts teaching Chemistry, someone has to add three rows, one per language. Add two and the table now "says" she teaches Chemistry in English and Kiswahili but not Dholuo, which nobody meant.
- Her languages are written six times.

The trouble is two **independent** lists about the same tutor stored in one table. A tutor's subjects don't depend on their languages, but the table forces every pairing. That's a **multivalued dependency**, and 4NF is the normal form that forbids it.

## What you'll use

**X ->> Y** ("X multi-determines Y") holds in R when, for each X value, the set of Y values is independent of everything else (call the rest Z): every Y value appears with every Z value.

```
tutor ->> subject     Achieng: {Maths, Physics} × {English, Kiswahili, Dholuo}  = 6 rows
tutor ->> language    always comes as a pair: if X ->> Y, then X ->> Z  (complementation)
```

- **Every FD is an MVD**: if X → Y, each X has one Y, which is trivially "independent". The reverse isn't true.
- **Trivial MVDs**: Y ⊆ X, or X ∪ Y = R (there's no Z left to be independent of).
- **4NF**: for every non-trivial MVD X ->> Y (FDs included), X is a superkey. It's BCNF with MVDs added, so a relation in 4NF is in BCNF, but not always the other way round (`tutor_offers` is the proof).
- **Decomposing**: split R on a violation X ->> Y into `X ∪ Y` and `R − (Y − X)`. That's lossless exactly because X ->> Y holds (that's Fagin's theorem: R = (X∪Y) ⋈ (X∪Z) if and only if X ->> Y). Repeat until no part has a violation.

You can't see an MVD in the column names: it's a fact about the business ("every teacher of a course uses every book of that course"). The data can disprove one, which is what `holds_mvd` checks, but never prove it.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS tuition;"
tools/mysql.sh tuition < phase-4-normalisation/day-050-fourth-normal-form/setup.sql
```

1. `starter/0-split.sql`: create `tutor_subjects` and `tutor_languages` (two-column primary keys) and fill them from `tutor_offers`.
2. `starter/1-rebuild.sql`: join them back. You should get exactly the 11 original rows.
3. `starter/2-achieng_adds_chemistry.sql`: record Achieng's Chemistry. One row. (How many did the old table need?)
4. `starter/mvd.py`: `holds_mvd`, `complement`, `is_trivial`, `violations`, `is_4nf`, `decompose_4nf`. `closure` is done for you.
5. `starter/answers.py`.
6. `pytest phase-4-normalisation/day-050-fourth-normal-form`

## The kata: Find the MVDs

In `starter/mvd.py`, write `mvds_in(r)`: every non-trivial `{a} ->> {b}` between single attributes that holds in the data, leaving out the ones that are plain FDs (a → b). On `tutor_offers` that's `tutor ->> language` and `tutor ->> subject`.

## When you're stuck

- **`holds_mvd` says yes to everything**: for each X value, compare the number of distinct (Y, rest) pairs with (distinct Y values) × (distinct rest values). They're equal only when every pairing is there.
- **The rebuild has too many rows**: join on `tutor`, and nothing else; if the same (tutor, subject) pair is in `tutor_subjects` twice, step 1 forgot `DISTINCT` (the primary key should have stopped you).
- **`decompose_4nf` loops forever**: inside a part, drop the MVD once `(Y ∩ part) − X` is empty or the MVD is trivial for that part.
- **The ABCD example gives AB, ACD**: the FD A → B is also an MVD, and it splits first. Keep going: inside ACD, A ->> C still breaks 4NF.
- **Did 5NF go missing?** Fifth normal form deals with *join dependencies*: a table that only splits losslessly into three or more parts. It's rare in practice. The textbooks cover it if you're curious; this course stops at 4NF.
