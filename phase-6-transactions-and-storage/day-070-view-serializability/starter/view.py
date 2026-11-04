"""Day 70: view serializability.

A schedule is a list of Op(kind, txn, item) from coursekit.schedules.parse. Today's schedules have no aborts;
commits are allowed and change nothing.
"""

from collections import Counter
from itertools import permutations

from coursekit.schedules import parse  # noqa: F401


def conflict_serializable(schedule):
    """Day 69's test: no cycle in the precedence graph. (Done for you.)"""
    ops = [o for o in schedule if o.kind in ("r", "w")]
    edges = {(a.txn, b.txn) for n, a in enumerate(ops) for b in ops[n + 1:]
             if a.txn != b.txn and a.item == b.item and "w" in (a.kind, b.kind)}
    nodes = {o.txn for o in ops}
    while nodes:
        sources = [t for t in nodes if not any(j == t and i in nodes for i, j in edges)]
        if not sources:
            return False
        nodes -= set(sources)
    return True


def reads(schedule):
    """Every read, as (reader, writer, item): the writer is the last transaction to write the item before the
    read (it can be the reader itself), or None if nobody has, so the read sees the initial value.
    A Counter, since the same read can happen more than once."""
    raise NotImplementedError("write this")


def final_writes(schedule):
    """For each item that is written: the transaction that writes it last. A dict item -> txn."""
    raise NotImplementedError("write this")


def view_equivalent(s1, s2):
    """The same reads and writes by the same transactions, every read seeing the same writer (or the initial
    value), and the same final writes."""
    raise NotImplementedError("write this")


def is_view_serializable(schedule):
    """View-equivalent to at least one serial schedule (each transaction's operations together, in their own
    order, transactions in some order)."""
    raise NotImplementedError("write this")


def blind_writes(schedule):
    """Writes of an item the transaction hasn't read before (in this schedule): (txn, item), in order."""
    raise NotImplementedError("write this")


def explain(schedule):
    """Kata: "conflict serializable", "view serializable only", or "not serializable"."""
    raise NotImplementedError("write this")
