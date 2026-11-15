# How we write code in this course

Ten habits for every answer you write here, in SQL or in Python. They're what makes code easy to check, easy to fix, and safe to hand to someone else.

**1. Know what "done" means before you start.** Read the task line at the top of the starter file and the day's Steps. Say to yourself what the answer must return: which columns, named what, in what order. That's exactly what the test checks. If two readings are possible, ask (or check the "When you're stuck" section) before writing.

**2. Write only what was asked.** One query for one task. No extra columns, no extra statements, no "while I'm here" changes to the table. Extra output makes the test fail, and extra changes surprise the next person.

**3. Make it readable.** One clause per line, short clear aliases, column names the brief asks for:

```sql
-- Bad: one long line, mystery aliases, every column
select * from towns a left join shops b on b.town_id=a.id where b.id is null;

-- Good
SELECT t.name AS town
FROM towns AS t
LEFT JOIN shops AS s ON s.town_id = t.id
WHERE s.id IS NULL      -- no shop matched, so the town has none
ORDER BY town;
```

`SELECT *` is fine at the `mysql>` prompt while you look around; a finished answer lists the columns it needs, unless the task asks for every column.

**4. Change only what the task needs.** Keep the task comment at the top of the starter. Match the style of the code around you. Delete any test query or leftover line you added and don't need.

**5. Wrong result? See it fail first.** Run the day's test and read the first failure: it shows what came back and what was expected. If no test catches the problem (your own project, Day 100), first write a small query or a pytest test that shows the wrong row, and only then fix the answer. Then run all the day's tests again.

**6. Before you call it done, run the checks:**

```bash
pytest phase-1-first-queries/day-004-matatu-stages            # the day's tests: all must pass
pip install ruff==0.17.5 && ruff check phase-7-beyond-mysql/day-081-python-meets-sql   # Python days only
```

Use the exact `pytest` command the day's README gives. Ruff is the course's linter (its settings are in `pyproject.toml`); fix what it reports in your lines.

**7. Comments say why, not what.** `-- no shop matched, so the town has none` helps; `-- select the name` doesn't. In Python, a function's docstring says what it takes, what it returns and when it raises.

**8. Don't hide errors.** In a stored procedure, catch an error, undo, and pass it on: `DECLARE EXIT HANDLER FOR SQLEXCEPTION BEGIN ROLLBACK; RESIGNAL; END;` (Day 65). In Python, never write `except: pass` or catch everything and print: catch the exception you expect, or let it go up. `with conn.transaction():` rolls back for you when an exception escapes.

```python
try:
    transfer(conn, "254711000001", "254733000003", 2000)
except Exception:
    print("oops")          # Bad: the money problem is now invisible
```

**9. Tests check, they don't just print.** If you write your own test in Python, it uses `assert` and fails when the code is wrong: `assert find_member(conn, "Akinyi Atieno") == [(5, "Akinyi Atieno", "Kisumu")]`. Printing the rows is a look, not a test.

**10. Never commit passwords or generated files.** Real database passwords live in `.env` (copied from `.env.example`), which Git ignores; `tools/mysql.sh` and `tools/psql.sh` read it. Don't commit `.venv/` or `__pycache__/` either. A commit message says what changed and why: `fix day 20: count shops with COUNT(s.id) so empty towns show 0`, not `update`.
