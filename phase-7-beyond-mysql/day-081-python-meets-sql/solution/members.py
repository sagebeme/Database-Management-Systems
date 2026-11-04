"""Day 81: Python meets SQL.

Every function takes an open psycopg connection, `conn`, made with autocommit=True: each statement commits on its
own unless you open a transaction with `with conn.transaction():`.

Never put a value into SQL text with an f-string, `+` or `%`. Pass it separately and let the driver send it.
"""

from psycopg import sql


def find_unsafe(conn, name):
    """DON'T copy this. It glues the name into the SQL, so the name can change the SQL. (Done for you.)"""
    with conn.cursor() as cur:
        cur.execute(f"SELECT id, name, county FROM members WHERE name = '{name}' ORDER BY id")
        return cur.fetchall()


def find_member(conn, name):
    """(id, name, county) of every member called exactly `name`, by id: the safe version of find_unsafe."""
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, county FROM members WHERE name = %s ORDER BY id", (name,))
        return cur.fetchall()


def add_member(conn, name, phone, county):
    """Add a member with no savings and return the new id."""
    with conn.cursor() as cur:
        cur.execute("INSERT INTO members (name, phone, county) VALUES (%s, %s, %s) RETURNING id",
                    (name, phone, county))
        return cur.fetchone()[0]


def members_in(conn, counties):
    """Names of the members in any of `counties` (a list), alphabetical. One query, whatever the list's length."""
    with conn.cursor() as cur:
        cur.execute("SELECT name FROM members WHERE county = ANY(%s) ORDER BY name", (list(counties),))
        return [row[0] for row in cur.fetchall()]


def transfer(conn, from_phone, to_phone, amount):
    """Move `amount` of savings between two members, by phone, and record it in transfers. All of it happens,
    or none of it. Raise ValueError for an amount that isn't positive, an unknown phone, or savings that
    aren't enough. Return the transfer's id."""
    if amount <= 0:
        raise ValueError("the amount must be positive")
    with conn.transaction(), conn.cursor() as cur:
        cur.execute("SELECT id, phone, savings FROM members WHERE phone = ANY(%s) ORDER BY id FOR UPDATE",
                    ([from_phone, to_phone],))
        found = {phone: (mid, savings) for mid, phone, savings in cur.fetchall()}
        if from_phone not in found or to_phone not in found:
            raise ValueError("no member with that phone")
        (from_id, savings), (to_id, _) = found[from_phone], found[to_phone]
        if savings < amount:
            raise ValueError("not enough savings")
        cur.execute("UPDATE members SET savings = savings - %s WHERE id = %s", (amount, from_id))
        cur.execute("UPDATE members SET savings = savings + %s WHERE id = %s", (amount, to_id))
        cur.execute("INSERT INTO transfers (from_id, to_id, amount) VALUES (%s, %s, %s) RETURNING id",
                    (from_id, to_id, amount))
        return cur.fetchone()[0]


SORTABLE = ("name", "county", "savings")


def top_members(conn, order_by, limit):
    """Kata: (name, county, savings) of the first `limit` members sorted by the column `order_by` (one of SORTABLE),
    largest first, ties by name. ValueError for any other column. Column names can't be parameters: use
    psycopg.sql.Identifier, and only after checking the name against SORTABLE."""
    if order_by not in SORTABLE:
        raise ValueError(f"can't sort by {order_by!r}")
    query = sql.SQL("SELECT name, county, savings FROM members ORDER BY {} DESC, name LIMIT %s").format(
        sql.Identifier(order_by))
    with conn.cursor() as cur:
        cur.execute(query, (limit,))
        return cur.fetchall()
