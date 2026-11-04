"""Day 67: isolation levels, tried for real.

Each experiment gets `connect`, a function that opens a NEW connection (autocommit on) to a database loaded with
setup.sql, the engine's name ("mysql" or "postgres"), and a level ("READ UNCOMMITTED", "READ COMMITTED",
"REPEATABLE READ" or "SERIALIZABLE"). Open two connections: A changes things, B is the transaction being
observed, at `level`. Close both before returning. End every transaction you start with COMMIT or ROLLBACK
(as SQL: cur.execute("COMMIT")).

The helpers at the top are done for you.
"""

import pymysql
import psycopg

ACCOUNT = "254711000001"


def begin(cur, engine, level):
    """Start a transaction at this isolation level. (Done for you.)"""
    if engine == "mysql":
        cur.execute(f"SET TRANSACTION ISOLATION LEVEL {level}")
        cur.execute("START TRANSACTION")
    else:
        cur.execute(f"BEGIN ISOLATION LEVEL {level}")


def short_waits(cur, engine):
    """Give up after 1 second when waiting for a lock, instead of 50. (Done for you.)"""
    if engine == "mysql":
        cur.execute("SET SESSION innodb_lock_wait_timeout = 1")
    else:
        cur.execute("SET lock_timeout = '1s'")


def blocked(do):
    """Run do(). Return (True, None) if it gave up waiting for a lock, else (False, what do() returned).
    (Done for you.) After a lock timeout, roll that connection's transaction back."""
    try:
        return False, do()
    except pymysql.err.OperationalError as e:
        if e.args[0] == 1205:
            return True, None
        raise
    except psycopg.errors.LockNotAvailable:
        return True, None


def read_one(cur, sql):
    """The single value a query returns. (Done for you.)"""
    cur.execute(sql)
    return cur.fetchone()[0]


def sees_uncommitted(connect, engine, level):
    """A starts a transaction and sets the balance to 9999 without committing. B, at `level`, reads the balance.
    Return True if B saw 9999. (B's read may be blocked: that counts as not seeing it.) Then roll A back."""
    a, b = connect(), connect()
    try:
        ca, cb = a.cursor(), b.cursor()
        short_waits(cb, engine)
        ca.execute("BEGIN" if engine == "postgres" else "START TRANSACTION")
        ca.execute(f"UPDATE accounts SET balance = 9999 WHERE phone = '{ACCOUNT}'")
        begin(cb, engine, level)
        was_blocked, seen = blocked(lambda: read_one(cb, f"SELECT balance FROM accounts WHERE phone = '{ACCOUNT}'"))
        cb.execute("ROLLBACK")
        ca.execute("ROLLBACK")
        return not was_blocked and seen == 9999
    finally:
        a.close()
        b.close()


def repeatable(connect, engine, level):
    """B, at `level`, reads the balance. A then adds 100 and commits (A's update may be blocked: then it rolls
    back). B reads the balance again and commits. Return True if B's two reads were the same."""
    a, b = connect(), connect()
    try:
        ca, cb = a.cursor(), b.cursor()
        short_waits(ca, engine)
        begin(cb, engine, level)
        first = read_one(cb, f"SELECT balance FROM accounts WHERE phone = '{ACCOUNT}'")
        ca.execute("BEGIN" if engine == "postgres" else "START TRANSACTION")
        was_blocked, _ = blocked(lambda: ca.execute(
            f"UPDATE accounts SET balance = balance + 100 WHERE phone = '{ACCOUNT}'"))
        ca.execute("ROLLBACK" if was_blocked else "COMMIT")
        second = read_one(cb, f"SELECT balance FROM accounts WHERE phone = '{ACCOUNT}'")
        cb.execute("COMMIT")
        return first == second
    finally:
        a.close()
        b.close()


def sees_phantom(connect, engine, level):
    """B, at `level`, counts trip 2's bookings. A then inserts a new booking for trip 2 (id one more than the
    biggest) and commits (or rolls back if it was blocked). B counts again and commits. Return True if the
    counts differ."""
    a, b = connect(), connect()
    try:
        ca, cb = a.cursor(), b.cursor()
        short_waits(ca, engine)
        begin(cb, engine, level)
        first = read_one(cb, "SELECT COUNT(*) FROM bookings WHERE trip_id = 2")
        ca.execute("BEGIN" if engine == "postgres" else "START TRANSACTION")
        was_blocked, _ = blocked(lambda: ca.execute(
            "INSERT INTO bookings (id, trip_id, passenger) "
            "SELECT COALESCE(MAX(id), 0) + 1, 2, 'Phantom' FROM bookings"))
        ca.execute("ROLLBACK" if was_blocked else "COMMIT")
        second = read_one(cb, "SELECT COUNT(*) FROM bookings WHERE trip_id = 2")
        cb.execute("COMMIT")
        return first != second
    finally:
        a.close()
        b.close()
