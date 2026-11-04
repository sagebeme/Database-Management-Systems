"""Day 72: timestamp ordering, the Thomas write rule, wait-die and wound-wait.

A schedule is a list of Op(kind, txn, item) from coursekit.schedules.parse. `ts` maps each transaction to its
timestamp: smaller is older. When `ts` is None, use default_timestamps(schedule).

Outcomes, one per operation, in schedule order:
    "ok"      the operation runs
    "abort"   this operation breaks the rules, so its transaction is rolled back here
    "ignore"  (Thomas write rule only) an out-of-date write, skipped; the transaction carries on
    "skip"    the transaction was already rolled back, so this operation never happens
An aborted transaction is not restarted today, and the timestamps it already set on items stay set.
"""

from itertools import permutations

from coursekit.schedules import parse  # noqa: F401


def default_timestamps(schedule):
    """Timestamps in order of each transaction's first operation: the first to show up gets 1, the next 2, ..."""
    raise NotImplementedError("write this")


def basic_to(schedule, ts=None):
    """Basic timestamp ordering. For each item keep RTS (the largest timestamp that read it) and WTS (the
    largest that wrote it), both 0 at the start.
        read:  too late if ts < WTS, otherwise RTS = max(RTS, ts)
        write: too late if ts < RTS or ts < WTS, otherwise WTS = ts
    Commits are "ok" (or "skip"). Returns the list of outcomes."""
    raise NotImplementedError("write this")


def thomas_write_rule(schedule, ts=None):
    """Basic timestamp ordering, except a write with ts < WTS (and ts >= RTS) is "ignore"d instead of aborting:
    a younger transaction has already written the item, so this write would be overwritten anyway."""
    raise NotImplementedError("write this")


def _run(schedule, ts, thomas):
    """Optional: write the rules once here and call it from basic_to and thomas_write_rule."""
    raise NotImplementedError("write this")


def aborted(outcomes, schedule):
    """The transactions that were rolled back, in the order it happened."""
    raise NotImplementedError("write this")


def wait_die(requester, holder, ts):
    """`requester` wants a lock `holder` has. Wait-die: an older requester "wait"s; a younger one "die"s
    (rolls back and restarts later with its old timestamp)."""
    raise NotImplementedError("write this")


def wound_wait(requester, holder, ts):
    """Wound-wait: an older requester "wound"s the holder (the holder rolls back); a younger one "wait"s."""
    raise NotImplementedError("write this")


def fewest_aborts(schedule):
    """Kata: try every way of giving the transactions the timestamps 1, 2, 3, ... and run basic_to with each.
    Return (order, aborts): the transactions oldest first, as a tuple, for the order that aborts the fewest,
    and that number. Ties go to the smallest tuple."""
    raise NotImplementedError("write this")
