"""Day 67 kata: the level's own test.

Run on a database loaded with setup.sql. Use the helpers in levels.py (import them).
"""

from levels import begin, short_waits, blocked, read_one, ACCOUNT  # noqa: F401

import pymysql
import psycopg


def write_skew(connect, engine, level):
    """Write skew. The ward's rule: at least one doctor must be on call. Dr Achieng (connection A) and
    Dr Barasa (B) both want the night off. Each starts a transaction at `level` and counts the doctors on call
    (2). Seeing 2, each takes themselves off call: A updates her row, then B updates his (either may be blocked
    or refused). Then A commits, then B. A blocked or refused statement or commit rolls that transaction back.
    Return how many doctors are on call at the end (counted with a fresh connection)."""
    a, b = connect(), connect()
    on_call = "SELECT COUNT(*) FROM doctors WHERE on_call"
    try:
        ca, cb = a.cursor(), b.cursor()
        doctors = {"Dr Achieng": ca, "Dr Barasa": cb}
        for cur in doctors.values():
            short_waits(cur, engine)
            begin(cur, engine, level)
        going = {name: cur for name, cur in doctors.items() if read_one(cur, on_call) >= 2}
        for name, cur in list(going.items()):
            try:
                was_blocked, _ = blocked(lambda: cur.execute(
                    f"UPDATE doctors SET on_call = FALSE WHERE name = '{name}'"))
            except (pymysql.err.OperationalError, psycopg.errors.SerializationFailure):
                was_blocked = True
            if was_blocked:
                cur.execute("ROLLBACK")
                del going[name]
        for name, cur in doctors.items():
            try:
                cur.execute("COMMIT")
            except psycopg.errors.SerializationFailure:
                cur.execute("ROLLBACK")
    finally:
        a.close()
        b.close()
    check = connect()
    try:
        return read_one(check.cursor(), on_call)
    finally:
        check.close()
