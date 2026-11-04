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
    found, last = Counter(), {}
    for op in schedule:
        if op.kind == "r":
            found[(op.txn, last.get(op.item), op.item)] += 1
        elif op.kind == "w":
            last[op.item] = op.txn
    return found


def final_writes(schedule):
    """For each item that is written: the transaction that writes it last. A dict item -> txn."""
    return {op.item: op.txn for op in schedule if op.kind == "w"}


def view_equivalent(s1, s2):
    """The same reads and writes by the same transactions, every read seeing the same writer (or the initial
    value), and the same final writes."""
    ops = lambda s: Counter((o.kind, o.txn, o.item) for o in s if o.kind in ("r", "w"))
    return ops(s1) == ops(s2) and reads(s1) == reads(s2) and final_writes(s1) == final_writes(s2)


def is_view_serializable(schedule):
    """View-equivalent to at least one serial schedule (each transaction's operations together, in their own
    order, transactions in some order)."""
    txns = sorted({o.txn for o in schedule if o.kind in ("r", "w")})
    for order in permutations(txns):
        serial = [o for t in order for o in schedule if o.txn == t and o.kind in ("r", "w")]
        if view_equivalent(schedule, serial):
            return True
    return False


def blind_writes(schedule):
    """Writes of an item the transaction hasn't read before (in this schedule): (txn, item), in order."""
    found, read = [], set()
    for op in schedule:
        if op.kind == "r":
            read.add((op.txn, op.item))
        elif op.kind == "w" and (op.txn, op.item) not in read and (op.txn, op.item) not in found:
            found.append((op.txn, op.item))
    return found


def explain(schedule):
    """Kata: "conflict serializable", "view serializable only", or "not serializable"."""
    if conflict_serializable(schedule):
        return "conflict serializable"
    if is_view_serializable(schedule):
        return "view serializable only"
    return "not serializable"
