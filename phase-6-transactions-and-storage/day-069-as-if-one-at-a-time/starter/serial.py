"""Day 69: conflict serializability.

A schedule is a list of Op(kind, txn, item) from coursekit.schedules.parse. Commits and aborts don't conflict
with anything; only reads and writes do. A precedence graph is a dict: every transaction in the schedule maps to
the sorted list of transactions it must come before.
"""

from itertools import combinations, permutations

from coursekit.schedules import parse  # noqa: F401


def conflicts(schedule):
    """Every pair of conflicting operations: different transactions, the same item, at least one a write.
    As (i, j, item) for Ti's operation coming first, in the order the later operation appears, no repeats."""
    raise NotImplementedError("write this")


def precedence_graph(schedule):
    """Ti -> Tj for every conflict where Ti's operation comes first."""
    raise NotImplementedError("write this")


def has_cycle(graph):
    """Does the graph have a cycle?"""
    raise NotImplementedError("write this")


def is_conflict_serializable(schedule):
    """True when the precedence graph has no cycle."""
    raise NotImplementedError("write this")


def serial_orders(schedule):
    """Every serial order of the transactions the schedule is conflict-equivalent to: every order that puts Ti
    before Tj for each edge. A sorted list of tuples; empty if there's a cycle."""
    raise NotImplementedError("write this")


def conflict_equivalent(s1, s2):
    """Same operations (as a multiset, ignoring commits and aborts), and every conflicting pair in the same
    order."""
    raise NotImplementedError("write this")


def count_serializable(t1, t2):
    """Kata: t1 and t2 are two transactions' operations, in order. Of all the ways to interleave them (keeping
    each one's own order), how many are conflict serializable?"""
    raise NotImplementedError("write this")
