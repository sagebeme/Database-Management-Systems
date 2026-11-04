# Phase 4: Normalisation

Why some tables cause trouble and how to fix them: functional dependencies, keys found by closure, and splitting tables up to 4NF without losing data or rules. The most-asked part of GATE's databases section.

**You learn:** anomalies, functional dependencies, attribute closure, candidate keys, Armstrong's axioms, minimal covers, lossless and dependency-preserving decomposition, 1NF to 4NF.

**It ends with:** an M-Pesa agent's spreadsheet turned into a clean schema.

## The days

| Day | Project | What it teaches |
|---|---|---|
| 41 | [The Messy Spreadsheet](day-041-the-messy-spreadsheet/README.md) | insert, update and delete anomalies |
| 42 | [Does It Depend?](day-042-does-it-depend/README.md) | functional dependencies, checked against data |
| 43 | [Closure](day-043-closure/README.md) | attribute closure and finding every candidate key |
| 44 | [Same Rules, Different Words](day-044-same-rules-different-words/README.md) | Armstrong's axioms, implied and equivalent FD sets |
| 45 | [The Shortest Rulebook](day-045-the-shortest-rulebook/README.md) | minimal and canonical covers |
| 46 | [Splitting Without Losing](day-046-splitting-without-losing/README.md) | lossless-join decomposition |
| 47 | [Splitting Without Forgetting](day-047-splitting-without-forgetting/README.md) | dependency-preserving decomposition |
| 48 | [First and Second Normal Form](day-048-first-and-second-normal-form/README.md) | atomic values, partial dependencies |
| 49 | [Third Normal Form and BCNF](day-049-third-normal-form-and-bcnf/README.md) | transitive dependencies, 3NF synthesis, BCNF decomposition |
| 50 | [Fourth Normal Form](day-050-fourth-normal-form/README.md) | multivalued dependencies |
| 51 | [Breaking the Rules on Purpose](day-051-breaking-the-rules-on-purpose/README.md) | denormalisation, summary tables |
| 52 | [Capstone: The Agent's Ledger](day-052-capstone-the-agents-ledger/README.md) | normalise a real-looking spreadsheet and migrate the data |

## Outside the hundred days

These don't count towards the hundred days, and nothing later depends on them. They're there to make the theory stick.

- [worked-examples.md](worked-examples.md): nine problems (closure, every candidate key, minimal cover, the chase, dependency preservation, normal forms, 3NF synthesis, BCNF, 4NF) solved step by step.
- [Checkpoint 2: Practice Test 2](checkpoint-2-practice-test-2/README.md): a 26-mark paper on this phase. Take it after Day 52.

## How to test your work

**Run a day's tests:**

```bash
pytest phase-4-normalisation/day-043-closure                       # every test for the day
pytest phase-4-normalisation/day-043-closure -k kata               # only tests whose name contains "kata"
pytest phase-4-normalisation/day-043-closure -x --tb=short         # stop at the first failure, with a short explanation
```

Each test runs one of your files and compares the result with the right answer. A failure shows what came back and what was expected, usually as rows like `('Nakuru', '12')`. From SQL files, every value comes back as text, and `NULL` as `'NULL'`. Read the first failure only, fix it, run again.

**Many tests change the data and run your file a second time**, so an answer typed in by hand, or one that only works for today's rows, fails the second run. If the first run passes and the second fails, your query depends on something it shouldn't (an id you typed, a row's position, a name spelled out).

**Run your work by hand:**

Most days here are Python and `answers.py`, plus SQL where you migrate real data:

- **Dependencies are written as text**: `"AB->C; C->D"`. Try your functions at a Python prompt: `PYTHONPATH=tools python -i phase-4-normalisation/day-043-closure/starter/closure.py`, then `from coursekit.fds import parse` and `closure("A", parse("A->B; B->C"))`. (`PYTHONPATH=tools` lets Python find the course's helper package, `coursekit`, the way the tests do.)
- **`answers.py`**: replace each `None`. The tests say right or wrong, never the answer.
- **SQL files** run as in Phases 1 and 2: `tools/mysql.sh practice < phase-N-.../day-NNN-.../starter/0-something.sql`.

**Still stuck?** Read the day's "When you're stuck" section first: it lists the mistakes people actually make. Then open the same file in `solution/` and compare. It spoils the answer, so read it, close it, and write your own version from memory.

On Windows, run all of this in the Ubuntu (WSL) terminal, not PowerShell: see [WINDOWS.md](../WINDOWS.md).


## Further reading

- *Database System Concepts* ([db-book.com](https://db-book.com/)), chapter 7: relational database design.
- Past GATE CSE papers: normalisation appears almost every year.
