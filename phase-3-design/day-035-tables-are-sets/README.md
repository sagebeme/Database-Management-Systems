# Day 35: Tables Are Sets

## The brief

In 1970, Edgar Codd at IBM published the paper that every SQL database since has been built on. His idea: a table is a **relation**, the mathematical kind, which is a *set* of tuples. Everything you've done in SQL has a precise meaning in set theory, and that precision is why a database can rewrite your query into a faster one and promise the answer hasn't changed (Day 91).

The next four days are the maths. They're what GATE examines, and they make SQL's odd corners (duplicates, `NULL`s, why `DISTINCT` exists) make sense. Today you build a relation in Python and compare it with what MySQL actually gives you.

## What you'll use

| Everyday word | Relational term | Example |
|---|---|---|
| table | **relation** | `towns` |
| row | **tuple** | `('Molo', 'Nakuru')` |
| column | **attribute** | `county` |
| the values a column may take | **domain** | the 47 county names |
| number of columns | **degree** (or arity) | 2 |
| number of rows | **cardinality** | 8 |
| the definition | **relation schema** | `towns(name, county)` |
| the rows at one moment | **relation instance** (or state) | today's 8 towns |

Because a relation is a **set**:

- **There are no duplicate tuples.** A set holds each element once.
- **Tuples have no order.** `{a, b}` and `{b, a}` are the same set, which is why SQL promises no order without `ORDER BY` (Day 6).
- **Attributes have no order either**, when you know them by name: `(name, county)` and `(county, name)` describe the same relation if the values line up.

**SQL is not quite set theory.** An SQL table with no key can hold the same row twice, and `SELECT county FROM towns` returns `Nakuru` three times. SQL works with **bags** (multisets) unless you ask for `DISTINCT`, mainly because removing duplicates costs a sort, and sometimes you want the count. Relational algebra (Day 36) always works with sets.

In Python, a `frozenset` of tuples is a relation's body:

```python
rows = frozenset({("Molo", "Nakuru"), ("Thika", "Kiambu")})
("Molo", "Nakuru") in rows        # True
len(rows)                         # the cardinality
```

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS sets;"
tools/mysql.sh sets < phase-3-design/day-035-tables-are-sets/setup.sql
```

1. `starter/relations.py`: `make` (build a relation; refuse repeated attribute names and wrong-length rows; drop duplicates), `degree`, `cardinality`.
2. `same`: are two relations equal, whatever order their attributes are listed in? Reorder one's tuples to match the other's heading, then compare the sets.
3. `in_domains` and `from_result`.
4. `starter/0-counties_as_bag.sql`: every town's county, one row per town. `starter/1-counties_as_set.sql`: each county once.
5. `starter/answers.py`: the words.
6. `pytest phase-3-design/day-035-tables-are-sets`

## The kata: How Many Relations?

In `starter/relations.py`, write `possible_tuples(domain_sizes)` and `possible_relations(domain_sizes)`. If attribute A has 2 possible values and B has 3, how many different tuples could exist? And how many different relation instances? Every *subset* of those tuples is one, including the empty one.

## When you're stuck

- **`make` keeps duplicates**: lists aren't hashable and can't go in a set. Turn each row into a `tuple` first.
- **`same` says two equal relations differ**: for each attribute in r's heading, find its position in s's heading (`s.heading.index(a)`), then rebuild s's rows in that order.
- **The bag query returns 4 rows**: that's the set. Leave out `DISTINCT`.
- **`possible_relations` is far too small**: each tuple is either in an instance or not, two choices per tuple. That's 2 to the power of the number of tuples.
