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
    raise NotImplementedError("write this")


def add_member(conn, name, phone, county):
    """Add a member with no savings and return the new id."""
    raise NotImplementedError("write this")


def members_in(conn, counties):
    """Names of the members in any of `counties` (a list), alphabetical. One query, whatever the list's length."""
    raise NotImplementedError("write this")


def transfer(conn, from_phone, to_phone, amount):
    """Move `amount` of savings between two members, by phone, and record it in transfers. All of it happens,
    or none of it. Raise ValueError for an amount that isn't positive, an unknown phone, or savings that
    aren't enough. Return the transfer's id."""
    raise NotImplementedError("write this")


SORTABLE = ("name", "county", "savings")


def top_members(conn, order_by, limit):
    """Kata: (name, county, savings) of the first `limit` members sorted by the column `order_by` (one of SORTABLE),
    largest first, ties by name. ValueError for any other column. Column names can't be parameters: use
    psycopg.sql.Identifier, and only after checking the name against SORTABLE."""
    raise NotImplementedError("write this")
