"""Day 65 kata: Pay Day.

conn is a PyMySQL connection to the wallet database (autocommit off). payments is a list of (phone, amount).
"""


def pay_salaries(conn, payer, payments):
    """Pay every payment from payer, in ONE transaction. A payment that can't be made (not enough money left, or
    no such account) is skipped, using a SAVEPOINT so the others still go through. Record each payment that
    succeeds in transfers. Commit at the end. Return the phones that were skipped, in order."""
    raise NotImplementedError("write this")
