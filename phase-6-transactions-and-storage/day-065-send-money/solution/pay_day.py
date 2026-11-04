"""Day 65 kata: Pay Day.

conn is a PyMySQL connection to the wallet database (autocommit off). payments is a list of (phone, amount).
"""


def pay_salaries(conn, payer, payments):
    """Pay every payment from payer, in ONE transaction. A payment that can't be made (not enough money left, or
    no such account) is skipped, using a SAVEPOINT so the others still go through. Record each payment that
    succeeds in transfers. Commit at the end. Return the phones that were skipped, in order."""
    skipped = []
    with conn.cursor() as cur:
        cur.execute("START TRANSACTION")
        for phone, amount in payments:
            cur.execute("SAVEPOINT payment")
            taken = cur.execute("UPDATE accounts SET balance = balance - %s WHERE phone = %s AND balance >= %s",
                                (amount, payer, amount))
            given = taken and cur.execute("UPDATE accounts SET balance = balance + %s WHERE phone = %s",
                                          (amount, phone))
            if not given:
                cur.execute("ROLLBACK TO SAVEPOINT payment")
                skipped.append(phone)
                continue
            cur.execute("INSERT INTO transfers (from_phone, to_phone, amount) VALUES (%s, %s, %s)",
                        (payer, phone, amount))
    conn.commit()
    return skipped
