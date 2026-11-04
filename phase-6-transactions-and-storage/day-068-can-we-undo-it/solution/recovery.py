"""Day 68: can we undo it? Recoverable, cascadeless and strict schedules.

A schedule is a list of Op(kind, txn, item) from coursekit.schedules.parse. An aborted transaction's writes are
undone, so after a1, a read of an item T1 wrote sees whatever was there before T1's write.
"""

from coursekit.schedules import parse  # noqa: F401


def reads_from(schedule):
    """Every time a transaction reads a value written by ANOTHER transaction: (reader, writer, item), in order.
    The writer is the last transaction to write the item before the read, not counting writes undone by an
    abort. Reading your own write, or the initial value, isn't reading from anyone."""
    found, writers = [], {}
    for op in schedule:
        if op.kind == "w":
            writers.setdefault(op.item, []).append(op.txn)
        elif op.kind == "a":
            for item in writers:
                writers[item] = [t for t in writers[item] if t != op.txn]
        elif op.kind == "r":
            stack = writers.get(op.item, [])
            if stack and stack[-1] != op.txn:
                found.append((op.txn, stack[-1], op.item))
    return found


def is_recoverable(schedule):
    """Whenever Ti reads from Tj and Ti commits, Tj has committed before Ti's commit."""
    position = {}
    for n, op in enumerate(schedule):
        if op.kind in "ca":
            position.setdefault(op.txn, (op.kind, n))
    for reader, writer, _ in reads_from(schedule):
        if position.get(reader, ("", 0))[0] != "c":
            continue
        kind, when = position.get(writer, ("", len(schedule)))
        if kind != "c" or when > position[reader][1]:
            return False
    return True


def is_cascadeless(schedule):
    """Every read from another transaction happens after that writer has committed."""
    committed, writers = set(), {}
    for op in schedule:
        if op.kind == "c":
            committed.add(op.txn)
        elif op.kind == "a":
            for item in writers:
                writers[item] = [t for t in writers[item] if t != op.txn]
        elif op.kind == "w":
            writers.setdefault(op.item, []).append(op.txn)
        elif op.kind == "r":
            stack = writers.get(op.item, [])
            if stack and stack[-1] != op.txn and stack[-1] not in committed:
                return False
    return True


def is_strict(schedule):
    """No transaction reads or writes an item that another transaction has written, until that writer has
    committed or aborted."""
    finished, pending = set(), {}
    for op in schedule:
        if op.kind in ("c", "a"):
            finished.add(op.txn)
        elif op.kind in ("r", "w"):
            if any(t != op.txn and t not in finished for t in pending.get(op.item, [])):
                return False
            if op.kind == "w":
                pending.setdefault(op.item, []).append(op.txn)
    return True


def cascade(schedule, aborting):
    """If `aborting` aborts, every transaction that read a value it wrote must abort too, and every one that
    read from those, and so on. Return them, sorted (not including `aborting`)."""
    pairs = reads_from(schedule)
    doomed = {aborting}
    grew = True
    while grew:
        grew = False
        for reader, writer, _ in pairs:
            if writer in doomed and reader not in doomed:
                doomed.add(reader)
                grew = True
    return sorted(doomed - {aborting})


def classify(schedule):
    """Kata: the strongest that holds: "strict", "cascadeless", "recoverable" or "not recoverable"."""
    if is_strict(schedule):
        return "strict"
    if is_cascadeless(schedule):
        return "cascadeless"
    if is_recoverable(schedule):
        return "recoverable"
    return "not recoverable"
