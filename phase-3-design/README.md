# Phase 3: Designing databases

Before you write a table you design it. This phase is the theory behind tables: keys, integrity, ER diagrams, and the maths of relational algebra and calculus, the core of GATE's databases questions.

**You learn:** why a DBMS beats files, keys, integrity constraints, ER diagrams, cardinality, weak entities, the relational model, relational algebra, tuple and domain relational calculus.

**It ends with:** a hospital database designed from a brief.

## The days

| Day | Project | What it teaches |
|---|---|---|
| 29 | [The Exercise Book Problem](day-029-the-exercise-book-problem/README.md) | files vs a DBMS, built in Python |
| 30 | [Which Column Is the Key?](day-030-which-column-is-the-key/README.md) | super, candidate, primary, alternate and foreign keys |
| 31 | [Rules the Database Enforces](day-031-rules-the-database-enforces/README.md) | domain, entity and referential integrity |
| 32 | [Drawing the Shop](day-032-drawing-the-shop/README.md) | ER diagrams: entities, attributes, relationships |
| 33 | [One, Many, Many-to-Many](day-033-one-many-many-to-many/README.md) | cardinality, participation, the fewest tables |
| 34 | [Dependants and Managers](day-034-dependants-and-managers/README.md) | weak entities, self-referential relationships |
| 35 | [Tables Are Sets](day-035-tables-are-sets/README.md) | the relational model in maths |
| 36 | [Relational Algebra I](day-036-relational-algebra-i/README.md) | select, project, rename, union, difference, product |
| 37 | [Relational Algebra II](day-037-relational-algebra-ii/README.md) | joins and division |
| 38 | [Relational Calculus](day-038-relational-calculus/README.md) | tuple and domain calculus, safe queries |
| 39 | [Practice Test 1](day-039-practice-test-1/README.md) | GATE-style questions on Phases 1–3 |
| 40 | [Capstone: Design a Hospital](day-040-capstone-design-a-hospital/README.md) | from a brief to an ER diagram, tables and queries |

## Outside the hundred days

These don't count towards the hundred days, and nothing later depends on them. They're there to make the theory stick.

- [worked-examples.md](worked-examples.md): eight exam problems (superkeys, fewest tables, join sizes, division, outer joins, calculus) solved step by step. Read them after Day 38.
- [Day 39: Practice Test 1](day-039-practice-test-1/README.md) is this phase's checkpoint.

## How to test your work

**Run a day's tests:**

```bash
pytest phase-3-design/day-036-relational-algebra-i                       # every test for the day
pytest phase-3-design/day-036-relational-algebra-i -k kata               # only tests whose name contains "kata"
pytest phase-3-design/day-036-relational-algebra-i -x --tb=short         # stop at the first failure, with a short explanation
```

Each test runs one of your files and compares the result with the right answer. A failure shows what came back and what was expected, usually as rows like `('Nakuru', '12')`. From SQL files, every value comes back as text, and `NULL` as `'NULL'`. Read the first failure only, fix it, run again.

**Many tests change the data and run your file a second time**, so an answer typed in by hand, or one that only works for today's rows, fails the second run. If the first run passes and the second fails, your query depends on something it shouldn't (an id you typed, a row's position, a name spelled out).

**Run your work by hand:**

This phase mixes kinds of work, and each runs differently:

- **SQL files** (`.sql`) run exactly as in Phases 1 and 2: `tools/mysql.sh practice < phase-N-.../day-NNN-.../starter/0-something.sql`.
- **Python files** (`.py`): relational algebra and calculus written as functions. Try them at a Python prompt from the course folder: `PYTHONPATH=tools python -i phase-3-design/day-036-relational-algebra-i/starter/algebra.py`, then call your functions. (`PYTHONPATH=tools` lets Python find the course's helper package, `coursekit`, the way the tests do.)
- **ER diagrams** (`.mmd`) are Mermaid. Paste one into [mermaid.live](https://mermaid.live) to see it drawn, or put it in a Markdown file on GitHub, which draws it for you. The tests read the diagram's text, so check the error message for the line it couldn't read.
- **`answers.py`** holds exam-style answers: replace each `None`. The tests only say right or wrong, never the answer.

**Still stuck?** Read the day's "When you're stuck" section first: it lists the mistakes people actually make. Then open the same file in `solution/` and compare. It spoils the answer, so read it, close it, and write your own version from memory.

On Windows, run all of this in the Ubuntu (WSL) terminal, not PowerShell: see [WINDOWS.md](../WINDOWS.md).


## Further reading

- [Mermaid ER diagram syntax](https://mermaid.js.org/syntax/entityRelationshipDiagram.html).
- *Database System Concepts* by Silberschatz, Korth and Sudarshan ([db-book.com](https://db-book.com/)): chapters 2 and 6 cover this phase, with slides.
- Past GATE CSE papers, published by the IIT organising each year's exam: do the database questions after Practice Test 1.
