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
    found, earlier = [], []
    for op in schedule:
        if op.kind not in ("r", "w"):
            continue
        for prev in earlier:
            if prev.txn != op.txn and prev.item == op.item and "w" in (prev.kind, op.kind):
                pair = (prev.txn, op.txn, op.item)
                if pair not in found:
                    found.append(pair)
        earlier.append(op)
    return found


def precedence_graph(schedule):
    """Ti -> Tj for every conflict where Ti's operation comes first."""
    graph = {t: set() for t in sorted({op.txn for op in schedule})}
    for i, j, _ in conflicts(schedule):
        graph[i].add(j)
    return {t: sorted(after) for t, after in graph.items()}


def has_cycle(graph):
    """Does the graph have a cycle?"""
    state = {t: "new" for t in graph}

    def visit(t):
        state[t] = "visiting"
        for u in graph.get(t, []):
            if state.get(u) == "visiting" or (state.get(u) == "new" and visit(u)):
                return True
        state[t] = "done"
        return False

    return any(state[t] == "new" and visit(t) for t in graph)


def is_conflict_serializable(schedule):
    """True when the precedence graph has no cycle."""
    return not has_cycle(precedence_graph(schedule))


def serial_orders(schedule):
    """Every serial order of the transactions the schedule is conflict-equivalent to: every order that puts Ti
    before Tj for each edge. A sorted list of tuples; empty if there's a cycle."""
    graph = precedence_graph(schedule)
    return sorted(order for order in permutations(graph)
                  if all(order.index(i) < order.index(j) for i in graph for j in graph[i]))


def conflict_equivalent(s1, s2):
    """Same operations (as a multiset, ignoring commits and aborts), and every conflicting pair in the same
    order."""
    ops = lambda s: sorted((o.kind, o.txn, o.item) for o in s if o.kind in ("r", "w"))
    return ops(s1) == ops(s2) and set(conflicts(s1)) == set(conflicts(s2))


def count_serializable(t1, t2):
    """Kata: t1 and t2 are two transactions' operations, in order. Of all the ways to interleave them (keeping
    each one's own order), how many are conflict serializable?"""
    t1, t2 = list(t1), list(t2)
    n = len(t1) + len(t2)
    count = 0
    for slots in combinations(range(n), len(t1)):
        a, b, schedule = iter(t1), iter(t2), []
        for k in range(n):
            schedule.append(next(a) if k in slots else next(b))
        count += is_conflict_serializable(schedule)
    return count
