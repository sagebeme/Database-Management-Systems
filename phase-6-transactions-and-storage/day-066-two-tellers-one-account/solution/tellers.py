"""Day 66: two tellers, one account.

conn is a PyMySQL connection with autocommit on. pause() is called where a slow teller (or a slow network)
would leave a gap; the tests pass one that sleeps, to make the race happen every time.
"""


def no_pause():
    pass


def withdraw_unsafe(conn, phone, amount, pause=no_pause):
    """(Done for you, and wrong.) Read the balance, check it, write the new balance."""
    with conn.cursor() as cur:
        cur.execute("SELECT balance FROM accounts WHERE phone = %s", (phone,))
        (balance,) = cur.fetchone()
        if balance < amount:
            return False
        pause()
        cur.execute("UPDATE accounts SET balance = %s WHERE phone = %s", (balance - amount, phone))
    return True


def withdraw_atomic(conn, phone, amount, pause=no_pause):
    """Take amount from the account in ONE statement that checks and changes together. True if it was taken,
    False if there wasn't enough."""
    pause()
    with conn.cursor() as cur:
        changed = cur.execute("UPDATE accounts SET balance = balance - %s WHERE phone = %s AND balance >= %s",
                              (amount, phone, amount))
    return changed == 1


def withdraw_locked(conn, phone, amount, pause=no_pause):
    """The read-check-write version, made safe: in a transaction, read the balance with SELECT ... FOR UPDATE,
    call pause(), then write it and commit (or roll back if there isn't enough). True if it was taken."""
    with conn.cursor() as cur:
        cur.execute("START TRANSACTION")
        cur.execute("SELECT balance FROM accounts WHERE phone = %s FOR UPDATE", (phone,))
        (balance,) = cur.fetchone()
        if balance < amount:
            conn.rollback()
            return False
        pause()
        cur.execute("UPDATE accounts SET balance = %s WHERE phone = %s", (balance - amount, phone))
    conn.commit()
    return True
