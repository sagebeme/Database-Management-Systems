# Day 36: Relational Algebra I

## The brief

Every SQL query you've written is, underneath, a short expression in **relational algebra**: a handful of operators that each take relations and give back a relation. MySQL's optimiser turns your SQL into this algebra, rearranges it into a cheaper form, then runs it (Day 91). GATE papers ask you to read and write it directly.

Today you write the six basic operators in Python, on Day 35's relations, then answer Riverwood questions by combining them, with no SQL at all.

## What you'll use

| Operator | Symbol | Does | SQL |
|---|---|---|---|
| select | σ<sub>p</sub>(R) | tuples of R where p is true | `WHERE p` |
| project | π<sub>A,B</sub>(R) | only attributes A, B (duplicates vanish) | `SELECT DISTINCT A, B` |
| rename | ρ<sub>a→b</sub>(R) | attribute a is now called b | `AS` |
| union | R ∪ S | tuples in either | `UNION` |
| difference | R − S | tuples in R but not S | `EXCEPT` (MySQL 8.0.31+) |
| product | R × S | every tuple of R paired with every tuple of S | `FROM R, S` / `CROSS JOIN` |

These six are the **basic** (fundamental) operators: none can be built from the others. Everything else is derived. Intersection, for example, is R ∩ S = R − (R − S).

- **σ doesn't change the heading; π does.** σ picks rows, π picks columns. Because π returns a set, π<sub>channel</sub>(SHOWS) has 3 tuples, not 8.
- **∪ and − need union-compatible relations**: the same attributes, with compatible domains.
- **× needs distinct attribute names.** To pair a relation with itself, rename one copy first. That's how you compare two shows.
- **Expressions nest**, innermost first: π<sub>title</sub>(σ<sub>channel='Bahari TV'</sub>(SHOWS)) selects, then projects.

Sizes, for exam questions (R and S union-compatible):

| Expression | Fewest tuples | Most tuples |
|---|---|---|
| σ(R) | 0 | \|R\| |
| π(R) | 1 (if R isn't empty) | \|R\| |
| R ∪ S | max(\|R\|, \|S\|) | \|R\| + \|S\| |
| R − S | max(0, \|R\| − \|S\|) | \|R\| |
| R × T | \|R\| × \|T\| | \|R\| × \|T\| |

The degree of R × T is degree(R) + degree(T).

`from coursekit.relational import make, same, show` gives you Day 35's relations, finished. `print(show(r))` draws one as a table.

## Steps

1. `starter/algebra.py`: the six operators. Each returns a new relation built with `make`.
2. `titles_on_bahari`, `comedy_or_drama`, `without_genre`: the queries in their docstrings, using only your operators.
3. `same_channel_pairs`: rename two copies of `shows` so no attribute names clash, take the product, select matching channels with `first < second`, project.
4. `starter/answers.py`: sizes and facts.
5. `pytest phase-3-design/day-036-relational-algebra-i`

## The kata: Only Minus

In `starter/algebra.py`, write `intersection(r, s)` using `difference` and nothing else: no `&`, no `in`.

## When you're stuck

- **`select` passes tuples to the predicate**: build a dict for each row with `dict(zip(r.heading, row))`.
- **`union` gives wrong rows when attributes are in a different order**: reorder s's tuples to r's heading first. `_aligned` does this for you.
- **`product` says the attributes clash**: in `same_channel_pairs`, rename *every* attribute of each copy (`title→first, channel→c1, year→y1` and `title→second, channel→c2, year→y2`).
- **Each pair appears twice**: `first < second` keeps one of (A, B) and (B, A), and also drops pairing a show with itself.
- **`FEWEST_TUPLES_IN_R_MINUS_S`**: at worst, all 6 tuples of S are also in R.
