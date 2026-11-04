# Day 43: Closure

## The brief

Day 30 asked "which column is the key?" and answered from meaning. With functional dependencies, you can *compute* the answer. Given a relation and its FDs, one simple algorithm, **attribute closure**, tells you everything a set of attributes determines. From that come superkeys, candidate keys, prime attributes, and (from Day 48) every normal form test.

It's the single most examined skill in GATE's normalisation questions, so today you write it, use it to find every key, and practise it on paper until it's automatic.

## What you'll use

**The closure X⁺** is every attribute X determines:

```
R(A, B, C, D, E),  F = { A → B,  BC → E,  ED → A }

{A, C}⁺:   start         A C
           A → B         A B C          (A is in what we have, so add B)
           BC → E        A B C E        (B and C are both in)
           ED → A        no: D is missing
           nothing new   {A, C}⁺ = ABCE  (no D, so AC is not a key)
```

- **X is a superkey** if X⁺ contains every attribute.
- **X is a candidate key** if it's a superkey and no proper subset is. Checking each subset with one attribute removed is enough.
- **Prime attribute**: belongs to some candidate key.

**Finding every candidate key** without trying all 2ⁿ subsets:

1. An attribute on **no right side** can't be determined by anything else, so it's in **every** key. Call these the core.
2. An attribute **only on right sides** (never on a left) is in **no** key.
3. If the core's closure is everything, the core is the only key. Otherwise, add the remaining attributes one, two, three at a time, skipping any set that contains a key already found.

In the example: C and D are on no right side, so every key contains CD. {C, D}⁺ = CD, which isn't enough. Try adding one more: ACD, BCD and CDE are all keys. Three candidate keys.

`from coursekit.fds import parse, attrs` turns `"A->B; BC->E"` into FDs and `"ACD"` into a set.

## Steps

1. `starter/closure.py`, `closure`: loop until nothing changes.
2. `is_superkey`, `is_candidate_key`.
3. `candidate_keys`: the three-step method above. The test with 14 attributes must run quickly, which brute force won't.
4. `prime_attributes`.
5. `starter/answers.py`: work these **on paper first**, then check with your code.
6. `pytest phase-4-normalisation/day-043-closure`

## The kata: Count Them

In `starter/closure.py`, write `count_superkeys(schema, fds)`: find the candidate keys, then count the superkeys with Day 30's inclusion–exclusion.

## When you're stuck

- **`closure` stops too early**: one pass isn't enough, because an FD skipped early can apply once later FDs have added attributes. Repeat the whole pass until nothing changes.
- **`closure` returns a `set`**: return `frozenset(...)` so it can be compared and stored in sets.
- **`candidate_keys` returns ABCD as well as ACD**: skip any set containing a key you've already found, and try smaller sets first.
- **`candidate_keys` with no FDs**: nothing determines anything, so the only key is the whole schema.
- **The 14-attribute test is slow**: you're trying every subset of everything. Only add attributes from the "maybe" group (on both sides) to the core.
