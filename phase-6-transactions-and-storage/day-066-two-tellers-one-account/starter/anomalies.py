"""Day 66: spotting anomalies in a schedule.

A schedule is a list of Op(kind, txn, item) from coursekit.schedules.parse, e.g. parse("r1(A) w2(A) c2 r1(A)").
Each function returns a list of (i, j, item) tuples, in the order the anomaly is completed in the schedule,
with no repeats.
"""

from coursekit.schedules import parse  # noqa: F401  (handy in the shell)


def dirty_reads(schedule):
    """Ti reads item, and the last write to item before that read was by another transaction Tj that hadn't
    committed yet. Returns (i, j, item)."""
    raise NotImplementedError("write this")


def non_repeatable_reads(schedule):
    """Ti reads item, another transaction Tj writes item, then Ti reads item again. Returns (i, j, item)."""
    raise NotImplementedError("write this")


def lost_updates(schedule):
    """Ti reads item, another transaction Tj writes item, then Ti writes item without reading it again, so
    Tj's write is overwritten by a value Ti worked out before it. Returns (i, j, item): Tj's update is lost."""
    raise NotImplementedError("write this")
