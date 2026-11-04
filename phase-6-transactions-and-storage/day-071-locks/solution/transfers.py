"""Day 71: deadlocks in real MySQL.

conn is a PyMySQL connection with autocommit on. pause() is called between locking the first account and the
second, which is where two transfers in opposite directions catch each other.
"""


def no_pause():
    pass


def transfer_naive(conn, from_phone, to_phone, amount, pause=no_pause):
    """(Done for you, and deadlock-prone.) Lock the sender, pause, lock the receiver, move the money."""
    with conn.cursor() as cur:
        cur.execute("START TRANSACTION")
        cur.execute("SELECT balance FROM accounts WHERE phone = %s FOR UPDATE", (from_phone,))
        pause()
        cur.execute("SELECT balance FROM accounts WHERE phone = %s FOR UPDATE", (to_phone,))
        cur.execute("UPDATE accounts SET balance = balance - %s WHERE phone = %s", (amount, from_phone))
        cur.execute("UPDATE accounts SET balance = balance + %s WHERE phone = %s", (amount, to_phone))
    conn.commit()


def transfer_ordered(conn, from_phone, to_phone, amount, pause=no_pause):
    """The same transfer, but lock the two accounts in one fixed order (the smaller phone number first),
    calling pause() between the two locks, so two transfers can never wait for each other in a circle."""
    first, second = sorted((from_phone, to_phone))
    with conn.cursor() as cur:
        cur.execute("START TRANSACTION")
        cur.execute("SELECT balance FROM accounts WHERE phone = %s FOR UPDATE", (first,))
        pause()
        cur.execute("SELECT balance FROM accounts WHERE phone = %s FOR UPDATE", (second,))
        cur.execute("UPDATE accounts SET balance = balance - %s WHERE phone = %s", (amount, from_phone))
        cur.execute("UPDATE accounts SET balance = balance + %s WHERE phone = %s", (amount, to_phone))
    conn.commit()


def transfer_with_retry(conn, from_phone, to_phone, amount, pause=no_pause, tries=5):
    """Use transfer_naive, but when MySQL picks it as a deadlock victim (error 1213), roll back and try again,
    up to `tries` times in all. Return how many attempts it took. Raise the last error if every try fails."""
    import pymysql

    for attempt in range(1, tries + 1):
        try:
            transfer_naive(conn, from_phone, to_phone, amount, pause)
            return attempt
        except pymysql.err.OperationalError as e:
            conn.rollback()
            if e.args[0] != 1213 or attempt == tries:
                raise
