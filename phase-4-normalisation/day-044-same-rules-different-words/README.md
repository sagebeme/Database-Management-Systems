# Day 44: Same Rules, Different Words

## The brief

Two analysts write down the FDs for the same school database. One writes `adm_no → name, class` and `class → teacher`. The other writes `adm_no → name`, `adm_no → class`, `adm_no → teacher` and `class → teacher`. Are they describing the same rules? You need to know before you design tables from either list.

FDs imply other FDs. If a student's admission number gives their class, and the class gives the teacher, then the admission number gives the teacher, whether anyone wrote it down or not. All the FDs a set implies form its **closure F⁺**. Two sets that imply exactly the same FDs are **equivalent**. Today: the rules for deriving FDs, and a fast test for both questions.

## What you'll use

**Armstrong's axioms.** These three rules derive every FD that follows from F (they're **complete**) and never one that doesn't (they're **sound**):

| Rule | From | Get |
|---|---|---|
| Reflexivity | Y ⊆ X | X → Y (trivial FDs) |
| Augmentation | X → Y | XZ → YZ |
| Transitivity | X → Y and Y → Z | X → Z |

Handy rules derived from those three:

| Rule | From | Get |
|---|---|---|
| Union | X → Y and X → Z | X → YZ |
| Decomposition | X → YZ | X → Y (and X → Z) |
| Pseudotransitivity | X → Y and WY → Z | WX → Z |

You can split a **right** side (decomposition), but never a **left** one: `AB → C` does *not* give `A → C`.

**You don't need the axioms to test implication.** Day 43's closure does it in one step: **X → Y follows from F exactly when Y ⊆ X⁺.** Listing F⁺ in full is exponential; one closure is fast.

**Equivalence**: F and G are equivalent if F implies every FD in G **and** G implies every FD in F. Both directions: F = {A → B, B → C} implies G = {A → B, A → C}, but G doesn't imply B → C, so they're not equivalent.

## Steps

1. `starter/axioms.py`: the three axioms and the three derived rules, each returning the FD it derives (or raising `ValueError` when it doesn't apply).
2. `implies`: one closure.
3. `equivalent`: both directions.
4. `starter/answers.py`: name the rule behind each step.
5. `pytest phase-4-normalisation/day-044-same-rules-different-words`

## The kata: Spot the Spare

In `starter/axioms.py`, write `redundant(fds)`: the FDs that follow from the others. Careful: in {A → B, B → A, A → C, B → C}, A → C and B → C are each spare, but you can't drop *both*. Tomorrow's minimal cover deals with that by removing them one at a time.

## When you're stuck

- **The FDs come back as the wrong type**: every side is a `frozenset`. `frozenset(x)` converts, and `a | b` on frozensets gives a frozenset.
- **`pseudotransitivity`**: W is fd2's left side with Y taken out: `fd2[0] - y`. The result's left side is W ∪ X.
- **`implies` misses an FD**: compute the closure of the FD's *left* side under F, then check the *right* side is inside it.
- **`equivalent` says yes when it shouldn't**: you checked only one direction.
