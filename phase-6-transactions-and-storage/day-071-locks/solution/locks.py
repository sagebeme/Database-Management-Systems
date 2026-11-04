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
    held = {}
    for op in schedule:
        mine = held.setdefault(op.item, {}) if op.item else None
        if op.kind == "sl":
            if any(t != op.txn and m == "X" for t, m in mine.items()):
                return False
            mine.setdefault(op.txn, "S")
        elif op.kind == "xl":
            if any(t != op.txn for t in mine):
                return False
            mine[op.txn] = "X"
        elif op.kind == "u":
            if op.txn not in mine:
                return False
            del mine[op.txn]
        elif op.kind == "r":
            if op.txn not in mine:
                return False
        elif op.kind == "w":
            if mine.get(op.txn) != "X":
                return False
        else:
            for locks in held.values():
                locks.pop(op.txn, None)
    return True


def follows_2pl(schedule):
    """Two-phase locking: no transaction takes a lock after its first unlock."""
    shrinking = set()
    for op in schedule:
        if op.kind == "u":
            shrinking.add(op.txn)
        elif op.kind in ("sl", "xl") and op.txn in shrinking:
            return False
    return True


def follows_strict_2pl(schedule):
    """2PL, and no exclusive lock is released before the transaction commits or aborts (an explicit unlock of
    an item the transaction holds exclusively, before its commit, breaks it)."""
    if not follows_2pl(schedule):
        return False
    exclusive = set()
    for op in schedule:
        if op.kind == "xl":
            exclusive.add((op.txn, op.item))
        elif op.kind == "u" and (op.txn, op.item) in exclusive:
            return False
        elif op.kind in ("c", "a"):
            exclusive = {(t, i) for t, i in exclusive if t != op.txn}
    return True


def deadlocked(holds, wants):
    """holds: {txn: {item: "S" or "X"}} (the locks each transaction holds). wants: {txn: (item, "S" or "X")}
    (the lock each blocked transaction is waiting for). Ti waits for Tj when Tj holds a lock on the item Ti
    wants that conflicts with the mode Ti wants. Return the transactions on a cycle of waiting, sorted
    ([] if there's no deadlock)."""
    waits = {t: set() for t in set(holds) | set(wants)}
    for t, (item, mode) in wants.items():
        for other, locks in holds.items():
            if other != t and item in locks and "X" in (mode, locks[item]):
                waits[t].add(other)
    on_cycle = set()
    for start in waits:
        stack, seen = [start], set()
        while stack:
            node = stack.pop()
            for nxt in waits.get(node, ()):
                if nxt == start:
                    on_cycle.add(start)
                elif nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
    return sorted(on_cycle)


def possible_under_rigorous_2pl(schedule):
    """Kata: could this schedule (reads, writes, commits; no lock operations) come out of rigorous 2PL, where
    every lock is held until commit? Add locks as late as possible (a shared lock just before a transaction's
    first read of an item, an exclusive lock just before its first write, upgrading if it already holds a
    shared one) and let each commit release everything. True if the result is well formed."""
    with_locks, held = [], set()
    for op in schedule:
        if op.kind == "r" and (op.txn, op.item) not in held:
            with_locks.append(Op("sl", op.txn, op.item))
            held.add((op.txn, op.item))
        elif op.kind == "w" and (op.txn, op.item, "X") not in held:
            with_locks.append(Op("xl", op.txn, op.item))
            held |= {(op.txn, op.item), (op.txn, op.item, "X")}
        with_locks.append(op)
    return is_well_formed(with_locks)
