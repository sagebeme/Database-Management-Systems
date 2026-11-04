"""Day 71: locks on paper.

A schedule is a list of Op(kind, txn, item) from coursekit.schedules.parse, with lock operations:
sl1(A) shared lock, xl1(A) exclusive lock, u1(A) unlock. A transaction holding a shared lock may take the
exclusive lock on the same item (an upgrade) if nobody else holds a lock on it.
"""

from coursekit.schedules import Op, parse  # noqa: F401


def is_well_formed(schedule):
    """Every read is covered by a shared or exclusive lock the reader holds; every write by an exclusive lock
    the writer holds; no lock is granted while another transaction holds a conflicting one (shared with shared
    is the only pair that doesn't conflict); a transaction only unlocks what it holds. A commit or abort
    releases everything the transaction still holds."""
    raise NotImplementedError("write this")


def follows_2pl(schedule):
    """Two-phase locking: no transaction takes a lock after its first unlock."""
    raise NotImplementedError("write this")


def follows_strict_2pl(schedule):
    """2PL, and no exclusive lock is released before the transaction commits or aborts (an explicit unlock of
    an item the transaction holds exclusively, before its commit, breaks it)."""
    raise NotImplementedError("write this")


def deadlocked(holds, wants):
    """holds: {txn: {item: "S" or "X"}} (the locks each transaction holds). wants: {txn: (item, "S" or "X")}
    (the lock each blocked transaction is waiting for). Ti waits for Tj when Tj holds a lock on the item Ti
    wants that conflicts with the mode Ti wants. Return the transactions on a cycle of waiting, sorted
    ([] if there's no deadlock)."""
    raise NotImplementedError("write this")


def possible_under_rigorous_2pl(schedule):
    """Kata: could this schedule (reads, writes, commits; no lock operations) come out of rigorous 2PL, where
    every lock is held until commit? Add locks as late as possible (a shared lock just before a transaction's
    first read of an item, an exclusive lock just before its first write, upgrading if it already holds a
    shared one) and let each commit release everything. True if the result is well formed."""
    raise NotImplementedError("write this")
