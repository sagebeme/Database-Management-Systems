# Day 81: Python Meets SQL

## The brief

Nobody types SQL into `psql` to run a SACCO. A web app or a script does it, and that's where most real database bugs and security holes live. Today you'll write the Python a SACCO's back office would use to find members, add them and move money, with **psycopg 3**, the standard Postgres driver.

The biggest lesson is one line long: **never build SQL by gluing strings together.** A member called Ng'ang'a breaks it, and an attacker who types `' OR '1'='1` into a search box reads everyone's savings. That's **SQL injection**, still near the top of the OWASP Top 10 more than 25 years after it was first described.

## What you'll use

Python's database drivers all follow the **DB-API** (PEP 249): connect, get a cursor, execute, fetch.

```python
import psycopg

with psycopg.connect("host=127.0.0.1 port=5434 user=postgres dbname=sacco", autocommit=True) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM members WHERE county = %s", ("Kisumu",))
        rows = cur.fetchall()        # [(2, 'Otieno Ochieng'), (5, 'Akinyi Atieno')]
```

PyMySQL (Day 66) works the same way: `pymysql.connect(...)`, `cur.execute(sql, params)`, `fetchall()`.

**Parameters**: write `%s` where a value goes and pass the values as a tuple (note the comma in `("Kisumu",)`). The driver keeps the value separate from the SQL; psycopg 3 sends them to the server separately, so a value can never become SQL. `%s` is used whatever the type: don't put quotes around it.

```python
cur.execute(f"... WHERE name = '{name}'")      # NO: name becomes part of the SQL
cur.execute("... WHERE name = %s", (name,))    # yes
```

- A Python list becomes a Postgres array: `WHERE county = ANY(%s)` with `(["Kisumu", "Nyeri"],)`.
- `INSERT ... RETURNING id`, then `cur.fetchone()[0]`, gets the new id.

**Names can't be parameters.** `ORDER BY %s` sorts by a constant string, not a column. When a column or table name must vary, check it against a list you wrote, then build the SQL with `psycopg.sql`:

```python
from psycopg import sql
query = sql.SQL("SELECT name FROM members ORDER BY {}").format(sql.Identifier(column))
```

**Transactions**: with `autocommit=True` each statement commits on its own. Group statements with

```python
with conn.transaction():
    ...   # commits at the end of the block; rolls back if an exception escapes it
```

Raise inside the block and everything in it is undone. Lock the rows you're about to change with `SELECT ... FOR UPDATE` (Day 71), or two transfers at once can both spend the same shillings.

### Where the password goes: the environment and `.env`

The connection string above has no password, because your practice Postgres doesn't need one. A real one does, and it must never be in the code: a password in a `.py` file is in every copy of the repo, in its history for ever, and on GitHub within seconds of a push, where bots scan new commits for exactly this.

Settings that change between computers, and every secret, come from **environment variables** instead. libpq, the library under psycopg, reads the standard ones by itself, so the code doesn't mention them at all:

```bash
export PGHOST=127.0.0.1 PGPORT=5434 PGUSER=sacco_app PGPASSWORD='…'
```

```python
import os
conn = psycopg.connect(dbname="sacco")                    # host, port, user and password from PG* variables
url = os.environ["DATABASE_URL"]                          # a setting the app can't run without: fail loudly if missing
pool_size = int(os.environ.get("POOL_SIZE", "5"))         # an optional one, with a default
```

Typing `export` in every new terminal gets old, so on your own computer the values live in a **`.env`** file instead: one `NAME=value` per line, next to the code. This course does exactly that. Open `.env.example` at the repo root, then read `setting()` in `tools/coursekit/__init__.py`: it takes a real environment variable first, then the `.env` value, then a default that matches `tools/devdb.sh`. Real servers (Docker, Render, CI) set real environment variables and have no `.env` at all.

The rules:

- **`.env` is in `.gitignore`**, before the first commit. Check with `git check-ignore -v .env`.
- **Commit `.env.example`** with every name and a placeholder or a safe default, never a real value. It's how the next developer finds out what to set.
- **One account per program, with only the privileges it needs** (Day 25). The back office's password shouldn't be able to drop tables.
- **Never print or log a secret**, not even in an error message.
- **A leaked password is changed, not deleted.** Removing it from the code leaves it in the git history and in every clone. `ALTER USER … IDENTIFIED BY …` (Day 25) first, then clean up.

### `requirements.txt` and its counterparts

`psycopg` isn't part of Python. It came from `pip install -r requirements.txt` when you set up the course. Open that file; it starts:

```text
pytest==9.2.0
PyMySQL==1.2.3
psycopg[binary]==3.3.7
```

| Written | Means |
|---|---|
| `psycopg==3.3.7` | exactly 3.3.7. This course pins every package, so your tests run against what CI ran. |
| `psycopg~=3.3.7` | 3.3.7 or a later 3.3.x: patches only |
| `psycopg>=3.3` | anything newer, including a 4.0 that may break you |
| `psycopg[binary]` | an **extra**: also install the prebuilt `psycopg-binary`, so you don't need a C compiler and the Postgres headers |

**The virtual environment.** `pip install` puts packages into one Python. The `.venv` folder you made at setup is a private Python for this project, so its versions can't clash with another project's, and Ubuntu and Debian refuse a plain `pip install` into the system Python anyway (`externally-managed-environment`). `.venv` is gitignored, like `node_modules`: never commit it, and delete and recreate it whenever it acts strangely or you upgrade Python.

**Packages your packages need.** `requirements.txt` lists what this course asked for; pip also installed what those need. `pip freeze` lists everything, with exact versions. Apps that need fully repeatable installs keep a **lock** of that whole list: `pip-compile` (from pip-tools) turns a short `requirements.in` into a fully pinned `requirements.txt`, and `uv` and Poetry write `uv.lock` and `poetry.lock`. Newer projects declare their dependencies in **`pyproject.toml`**'s `[project] dependencies` instead; this repo's `pyproject.toml` only configures pytest.

| Task | npm | pip (in the venv) | uv |
|---|---|---|---|
| Install everything | `npm ci` | `pip install -r requirements.txt` | `uv sync` |
| Add a package | `npm install redis` | `pip install redis`, then add it to `requirements.txt` yourself | `uv add redis` |
| What's installed | `npm ls` | `pip list` / `pip freeze` | `uv pip list` |
| What a package needs | `npm ls redis` | `pip show pymongo` (its `Requires:` line: `dnspython`) | `uv tree` |
| What's out of date | `npm outdated` | `pip list --outdated` | `uv pip list --outdated` |
| Known security problems | `npm audit` | `pip-audit -r requirements.txt` (`pip install pip-audit`) | same |

**Before adding a package, check it's the real one.** Look it up on pypi.org: who publishes it, when it started, how many releases. Attackers publish packages with names one letter off popular ones, and AI coding tools sometimes suggest packages that don't exist, which someone can then register.

## Steps

```bash
tools/psql.sh postgres -c "CREATE DATABASE sacco;"
tools/psql.sh sacco -f phase-7-beyond-mysql/day-081-python-meets-sql/setup.sql
```

1. Read `find_unsafe` in `starter/members.py`. Call it with `"Ng'ang'a Mwangi"` and watch it break. Work out a name that makes it return everyone, and put it in `starter/answers.py` as `ATTACK`.
2. `find_member`, `add_member`, `members_in`.
3. `transfer`: all or nothing. Lock both rows, check, update both, record it. A test makes the last step fail and checks the first ones are undone; another fires four transfers at once from four connections.
4. The rest of `starter/answers.py`.
5. `pytest phase-7-beyond-mysql/day-081-python-meets-sql`
6. **Explore**, inside the course's `.venv`:

   ```bash
   git check-ignore -v .env          # which .gitignore line keeps .env out of git
   pip show pymongo                  # its version, and what it needs (dnspython)
   pip freeze                        # everything installed, not only what requirements.txt asked for
   pip list --outdated               # newer releases than the pinned ones
   ```

## The kata: Sort by Anything (Safely)

In `starter/members.py`, write `top_members(conn, order_by, limit)`: sort by a column the caller chooses, from a fixed list. It's the classic "sortable table" feature, and the classic injection hole when it's done with an f-string.

## When you're stuck

- **`TypeError: not all arguments converted`** or **`query has 1 placeholder but 7 parameters`**: the parameters must be a tuple or list. `(name)` is just `name`; write `(name,)`.
- **`syntax error at or near "Kisumu"`**: you put quotes around `%s`. Leave them off.
- **`members_in` with an empty list fails**: `ANY(%s)` with an empty list is fine. `IN %s` isn't valid in psycopg 3.
- **The transfer test with the trigger leaves balances changed**: the updates and the insert must all be inside one `with conn.transaction():` block.
- **Four transfers at once all succeed**: read the balances with `SELECT ... FOR UPDATE` inside the transaction, so the second transfer waits for the first to finish before it checks.
- **`top_members` accepts `savings; DROP TABLE members`**: check `order_by` against `SORTABLE` *before* building anything.
