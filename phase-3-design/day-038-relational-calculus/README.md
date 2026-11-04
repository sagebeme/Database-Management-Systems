# Day 38: Relational Calculus

## The brief

Relational algebra says **how** to get an answer: select this, project that, then subtract. Relational **calculus** says only **what** the answer is: "the titles of shows for which there exists a Drama genre row". That's how SQL feels too: you describe the rows you want, and the database works out the steps.

Codd proved the two have exactly the same power: any query in one can be written in the other, as long as the calculus query is **safe**. Today you write calculus formulas, and run them, because a Python comprehension *is* tuple relational calculus.

## What you'll use

**Tuple relational calculus (TRC)**: variables stand for whole tuples.

```
{ s.title | s ∈ SHOWS ∧ ∃ g ∈ GENRES (g.title = s.title ∧ g.genre = 'Drama') }
  output    range         "there exists a genre row g such that ..."
```

```python
{s["title"] for s in shows
 if any(g["title"] == s["title"] and g["genre"] == "Drama" for g in genres)}
```

| Logic | Read | Python |
|---|---|---|
| ∧, ∨, ¬ | and, or, not | `and`, `or`, `not` |
| ∃ g ∈ R (P) | there is a g in R with P | `any(P for g in R)` |
| ∀ g ∈ R (P) | every g in R has P | `all(P for g in R)` |
| P → Q | if P then Q | `(not P) or Q` |
| ∀ x (P) ≡ ¬∃ x (¬P) | "all are" = "none isn't" | SQL's `NOT EXISTS (... NOT ...)` (Day 37) |

**∀ with →, and the empty case.** "Shows never rated below 7" is ∀ r ∈ RATINGS (r.title = s.title → r.rate ≥ 7). A show with **no** ratings makes every implication true (its premise is always false), so it qualifies: *vacuous truth*. That's logically right and practically surprising. If you mean "rated, and never below 7", add ∃ r (r.title = s.title).

**Domain relational calculus (DRC)**: variables stand for single values, one per attribute.

```
{ ⟨y⟩ | ∃ t, c ( ⟨t, c, y⟩ ∈ SHOWS ∧ c = 'Bahari TV' ) }       -- years of Bahari shows
```

In Python: `{y for (t, c, y) in shows if c == "Bahari TV"}`.

**Safety.** `{ t | ¬(t ∈ SHOWS) }` asks for every tuple that *isn't* a show: every possible string and number. That set is infinite, so the query is **unsafe**. A safe query only produces values that appear in the database or the query's constants (its *domain*). Notice Python won't even let you write the unsafe one: a comprehension must iterate over something finite. Safe TRC, safe DRC and relational algebra can express exactly the same queries (Codd's theorem).

## Steps

1. `starter/calculus.py`: `recent`, `has_drama`, `no_genre`: each docstring holds a formula; translate it.
2. `never_below_seven`: ∀ with →. Check the unrated show comes out, then write `never_below_seven_and_rated`.
3. `bahari_years`: domain calculus, on plain tuples.
4. `starter/answers.py`: safety and the vocabulary.
5. `pytest phase-3-design/day-038-relational-calculus`

## The kata: Every, Without Division

In `starter/calculus.py`, write `every_core_unit`: Day 37's division as one calculus formula, ∀ around ∃. Then compare the shape of your Python with Day 37's double `NOT EXISTS` SQL. It's the same query.

## When you're stuck

- **`has_drama` returns every show**: the `any(...)` must check *both* that the genre row belongs to this show and that it's Drama.
- **Mwisho wa Reli is missing from `never_below_seven`**: that's right if you wrote "rated and never below 7". The formula has no ∃, so `all()` over zero matching ratings is `True`.
- **`→` is confusing in Python**: `P → Q` is `(not P) or Q`. Here: `r["title"] != s["title"] or r["rate"] >= 7`.
- **`every_core_unit` with no core units returns nobody**: `all()` of nothing is `True`, so everyone who has registered qualifies. Start from the set of students in `registrations`.
