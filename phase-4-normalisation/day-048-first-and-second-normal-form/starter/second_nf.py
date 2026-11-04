"""Day 48: second normal form.

Schemas are frozensets of attribute names; FDs are (lhs, rhs) pairs of frozensets.
"""

from itertools import combinations


def closure(attributes, fds):
    """Day 43's attribute closure. (Done for you.)"""
    result = set(attributes)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= result and not rhs <= result:
                result |= rhs
                changed = True
    return frozenset(result)


def candidate_keys(schema, fds):
    """Day 43's candidate keys, sorted by size then name. (Done for you.)"""
    schema = frozenset(schema)
    on_right = frozenset().union(*(rhs - lhs for lhs, rhs in fds)) & schema
    on_left = frozenset().union(*(lhs for lhs, _ in fds)) & schema
    core, maybe, keys = schema - on_right, sorted(schema & on_right & on_left), []
    for size in range(len(maybe) + 1):
        for extra in combinations(maybe, size):
            x = core | frozenset(extra)
            if not any(k <= x for k in keys) and closure(x, fds) >= schema:
                keys.append(x)
    return sorted(keys, key=lambda k: (len(k), sorted(k)))


def non_prime(schema, fds):
    """The attributes in no candidate key."""
    raise NotImplementedError


def partial_dependencies(schema, fds):
    """Every partial dependency: (X, A) where X is a non-empty PROPER subset of some candidate
    key, A is non-prime, A is not in X, and A is in X+. Sorted by (sorted(X), A), no repeats."""
    raise NotImplementedError


def is_2nf(schema, fds):
    """True if there is no partial dependency."""
    raise NotImplementedError


def to_2nf(schema, fds):
    """Kata: Pull Them Out. Split into 2NF: for each minimal left side X of a partial
    dependency (smallest first), make a part X ∪ {every non-prime A with X -> A partially};
    those A's leave the main part. The main part is what's left (it keeps the keys).
    Return the parts as frozensets: the pulled-out parts in that order, then the main part."""
    raise NotImplementedError
