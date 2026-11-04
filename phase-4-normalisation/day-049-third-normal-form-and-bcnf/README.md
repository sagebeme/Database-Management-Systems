# Day 49: Third Normal Form and BCNF

## The brief

2NF removed facts that hang off *part* of a key. Two problems remain, and today's two normal forms deal with them.

**A fact about a non-key fact.** In `(adm_no, class, class_teacher)`, the teacher depends on the class, which depends on the student. Every student in Form 3 West repeats "Mr Kiprop". That's a **transitive dependency**, and 3NF forbids it.

**A key part that depends on a non-key.** At a tuition centre, each student takes each subject with one tutor (`student, subject → tutor`), and each tutor teaches one subject (`tutor → subject`). The table `(student, subject, tutor)` is in 3NF, yet "Mr Omondi teaches Maths" is still repeated for every student he has. BCNF forbids that too, but at a price you'll see.

## What you'll use

For every non-trivial FD X → A:

| Normal form | The rule | Forbids |
|---|---|---|
| **3NF** | X is a superkey, **or** A is prime | non-key → non-key (transitive) |
| **BCNF** | X is a superkey. No exceptions | anything determined by a non-superkey |

You only need to check the FDs in F itself, not all of F⁺. (For a *part* of a decomposition, you do need the FDs implied within it; that's why `bcnf_decompose` uses closures.)

```
R(A, B, C), F = {A → B, B → C}        key A.   B → C: B isn't a superkey, C isn't prime.  → 2NF
R(A, B, C), F = {AB → C, C → B}       keys AB, AC.  C → B: C isn't a superkey, but B is prime.  → 3NF, not BCNF
```

**BCNF decomposition** (always lossless; *not always* dependency preserving):

```
while some part R has a violation X → Y (X not a superkey of R, X⁺ adds attributes of R):
    replace R with  (X⁺ ∩ R)  and  R − (X⁺ − X)
```

Each split shares X, and X is a key of the first part, so it's lossless by Day 46's binary test.

**3NF synthesis** (always lossless *and* dependency preserving):

1. Take a minimal cover (Day 45) and merge FDs with the same left side.
2. Make a table X ∪ Y for each X → Y.
3. If no table contains a candidate key, add one table that's just a key. This step is what makes it lossless.
4. Drop any table contained in another.

**The trade.** `(student, subject, tutor)` with `student, subject → tutor` and `tutor → subject`: BCNF splits it into `(tutor, subject)` and `(student, tutor)`. That's lossless, but the rule "a student has one tutor per subject" now spans two tables (Day 47). 3NF keeps one table and accepts a little repetition. In practice, most designers aim for 3NF and take BCNF when it's free.

## Steps

1. `starter/normal_forms.py`, `is_3nf` and `is_bcnf`. Closure, candidate keys and minimal cover are given.
2. `bcnf_decompose`: look for violations inside each part (closures under *all* the FDs), split, repeat.
3. `synthesize_3nf`: the four steps.
4. `starter/answers.py`: work R1 to R5 on paper.
5. `pytest phase-4-normalisation/day-049-third-normal-form-and-bcnf`

## The kata: How Normal Is It?

In `starter/normal_forms.py`, write `highest_normal_form(schema, fds)`: `"BCNF"`, `"3NF"`, `"2NF"` or `"1NF"`. Test BCNF first, then 3NF, then look for a partial dependency (Day 48).

## When you're stuck

- **`is_3nf` says no for the tutor example**: `tutor → subject` is fine for 3NF because `subject` is prime (it's in the key `student, subject`).
- **`bcnf_decompose` never stops**: only split on an X whose closure *within the part* is bigger than X and smaller than the part.
- **The lossless check fails for your BCNF split**: the second part must keep X: `R − (X⁺ − X)`, not `R − X⁺`.
- **The 3NF synthesis isn't lossless**: you skipped step 3, the key table.
- **`R5` is 3NF?** All five attributes are prime (keys ACD, BCD, CDE), so 3NF can't fail. But `A → B` has a non-superkey on the left, so it isn't BCNF.
