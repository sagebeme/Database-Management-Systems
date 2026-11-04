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

## The kata: Sort by Anything (Safely)

In `starter/members.py`, write `top_members(conn, order_by, limit)`: sort by a column the caller chooses, from a fixed list. It's the classic "sortable table" feature, and the classic injection hole when it's done with an f-string.

## When you're stuck

- **`TypeError: not all arguments converted`** or **`query has 1 placeholder but 7 parameters`**: the parameters must be a tuple or list. `(name)` is just `name`; write `(name,)`.
- **`syntax error at or near "Kisumu"`**: you put quotes around `%s`. Leave them off.
- **`members_in` with an empty list fails**: `ANY(%s)` with an empty list is fine. `IN %s` isn't valid in psycopg 3.
- **The transfer test with the trigger leaves balances changed**: the updates and the insert must all be inside one `with conn.transaction():` block.
- **Four transfers at once all succeed**: read the balances with `SELECT ... FOR UPDATE` inside the transaction, so the second transfer waits for the first to finish before it checks.
- **`top_members` accepts `savings; DROP TABLE members`**: check `order_by` against `SORTABLE` *before* building anything.
