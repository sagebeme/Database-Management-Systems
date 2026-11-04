"""Day 66: spotting anomalies in a schedule.

A schedule is a list of Op(kind, txn, item) from coursekit.schedules.parse, e.g. parse("r1(A) w2(A) c2 r1(A)").
Each function returns a list of (i, j, item) tuples, in the order the anomaly is completed in the schedule,
with no repeats.
"""

from coursekit.schedules import parse  # noqa: F401  (handy in the shell)


def dirty_reads(schedule):
    """Ti reads item, and the last write to item before that read was by another transaction Tj that hadn't
    committed yet. Returns (i, j, item)."""
    found, last_writer, committed = [], {}, set()
    for op in schedule:
        if op.kind == "c":
            committed.add(op.txn)
        elif op.kind == "w":
            last_writer[op.item] = op.txn
        elif op.kind == "r":
            j = last_writer.get(op.item)
            if j is not None and j != op.txn and j not in committed and (op.txn, j, op.item) not in found:
                found.append((op.txn, j, op.item))
    return found


def non_repeatable_reads(schedule):
    """Ti reads item, another transaction Tj writes item, then Ti reads item again. Returns (i, j, item)."""
    found, since = [], {}
    for op in schedule:
        if op.kind == "r":
            key = (op.txn, op.item)
            for j in since.get(key, []):
                if (op.txn, j, op.item) not in found:
                    found.append((op.txn, j, op.item))
            since[key] = []
        elif op.kind == "w":
            for (i, item), writers in since.items():
                if item == op.item and i != op.txn and op.txn not in writers:
                    writers.append(op.txn)
    return found


def lost_updates(schedule):
    """Ti reads item, another transaction Tj writes item, then Ti writes item without reading it again, so
    Tj's write is overwritten by a value Ti worked out before it. Returns (i, j, item): Tj's update is lost."""
    found, stale = [], {}
    for op in schedule:
        if op.kind == "r":
            stale[(op.txn, op.item)] = []
        elif op.kind == "w":
            for j in stale.pop((op.txn, op.item), []):
                if (op.txn, j, op.item) not in found:
                    found.append((op.txn, j, op.item))
            for (i, item), writers in stale.items():
                if item == op.item and i != op.txn and op.txn not in writers:
                    writers.append(op.txn)
    return found
