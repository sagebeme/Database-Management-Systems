"""Day 42: functional dependencies, checked against rows (dicts)."""

from itertools import combinations


def is_trivial(lhs, rhs):
    """True if lhs -> rhs is trivial: everything on the right is already on the left."""
    return set(rhs) <= set(lhs)


def holds(rows, lhs, rhs):
    """True if lhs -> rhs holds in these rows: any two rows that agree on every lhs attribute
    also agree on every rhs attribute."""
    seen = {}
    for row in rows:
        key = tuple(row[a] for a in lhs)
        value = tuple(row[a] for a in rhs)
        if seen.setdefault(key, value) != value:
            return False
    return True


def violations(rows, lhs, rhs):
    """The lhs values (as tuples, sorted) that appear with more than one rhs value."""
    found = {}
    for row in rows:
        found.setdefault(tuple(row[a] for a in lhs), set()).add(tuple(row[a] for a in rhs))
    return sorted(k for k, v in found.items() if len(v) > 1)


def holding_fds(rows, attributes):
    """Kata: Find Them All. Every non-trivial FD X -> A that holds in the rows, where A is one
    attribute, X has one or two attributes, and X is minimal (no smaller part of X already
    determines A). Return (tuple of X in attributes order, A) pairs, sorted."""
    found = []
    for size in (1, 2):
        for lhs in combinations(attributes, size):
            for a in attributes:
                if a in lhs:
                    continue
                if any(set(x) < set(lhs) for x, b in found if b == a):
                    continue
                if holds(rows, lhs, [a]):
                    found.append((lhs, a))
    return sorted(found)
