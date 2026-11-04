# Day 45: The Shortest Rulebook

## The brief

The school's FD list has grown to fifteen rules, written by three people over two years. Some say the same thing twice, some are implied by others, and some have attributes on the left that don't matter: if `adm_no` alone gives the class, then `adm_no, name → class` has a spare `name`. Before designing tables (Day 49's 3NF synthesis starts from exactly this), you want the **shortest equivalent rulebook**.

That's a **minimal cover**: an FD set equivalent to F, with nothing you could remove.

## What you'll use

A set of FDs is **minimal** when:

1. every right side is a single attribute;
2. no left side has an **extraneous** attribute: removing it would change what the FDs imply;
3. no FD is **redundant**: implied by the others.

**The algorithm**, in this order:

```
F = { A → BC,  B → C,  A → B,  AB → C }

1. Split right sides:      A → B, A → C, B → C, AB → C        (A → B twice: keep one)
2. Extraneous attributes:  in AB → C, is B extraneous?  A⁺ = {A, B, C} ⊇ C, so yes:  A → C
                           (now A → C appears twice: keep one)
3. Redundant FDs:          A → C?  without it, A⁺ = {A, B, C} ⊇ C, so drop it.
                           A → B? B → C? both needed.
Minimal cover:  { A → B,  B → C }
```

- **a ∈ X is extraneous in X → Y** if (X − a)⁺ ⊇ Y, computed under the current F.
- **An FD X → Y is redundant** if X⁺, computed with that FD removed, ⊇ Y.
- **Order matters.** Remove extraneous attributes *before* redundant FDs. The other way round can leave an FD that becomes redundant only after its left side shrinks.
- **A minimal cover isn't unique.** For {A → B, B → A, A → C, B → C}, either A → C or B → C can go, but not both. Which survives depends on the order you check.

The **canonical cover** merges FDs with the same left side: {A → B, A → C} becomes {A → BC}. Textbooks differ on whether "minimal" or "canonical" comes first; GATE usually means the minimal cover with single right sides.

## Steps

1. `starter/cover.py`, `split_right`: split, and drop duplicates and trivial FDs.
2. `extraneous`: which left attributes are extraneous, each tested alone.
3. `minimal_cover`: the three steps. Re-check after every change, against the *current* list.
4. `canonical_cover`: merge equal left sides.
5. `starter/answers.py`: on paper first.
6. `pytest phase-4-normalisation/day-045-the-shortest-rulebook`

## The kata: Check the Cover

In `starter/cover.py`, write `is_minimal(fds)`, which checks all three conditions. The test runs it on your own `minimal_cover` results, which should all pass.

## When you're stuck

- **The property test says an FD is redundant**: in step 3, check each FD against the *remaining* list, which shrinks as you drop FDs. Checking against the original list can drop two FDs that each covered for the other.
- **An attribute is still extraneous**: after removing one attribute from a left side, try the remaining ones again with the new, smaller left side.
- **Duplicates after step 2**: shrinking AB → C to A → C can duplicate an existing A → C. Remove duplicates before step 3.
- **`canonical_cover` loses an FD**: merge right sides with `|`; don't overwrite them.
