"""Day 43: attribute closure, and every candidate key from a set of FDs.

FDs are (lhs, rhs) pairs of frozensets; coursekit.fds.parse("AB->C; C->D") builds them.
Attribute sets are frozensets of names.
"""

from itertools import combinations


def closure(attributes, fds):
    """X+: every attribute X determines. Start with X; while some FD's left side is inside
    what you have, add its right side. Stop when nothing changes."""
    result = set(attributes)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= result and not rhs <= result:
                result |= rhs
                changed = True
    return frozenset(result)


def is_superkey(x, schema, fds):
    """True if x determines every attribute of schema."""
    return closure(x, fds) >= frozenset(schema)


def is_candidate_key(x, schema, fds):
    """A superkey none of whose proper subsets is a superkey. (Checking each subset missing
    one attribute is enough.)"""
    return is_superkey(x, schema, fds) and not any(is_superkey(set(x) - {a}, schema, fds) for a in x)


def candidate_keys(schema, fds):
    """Every candidate key, as frozensets, sorted by size and then by sorted(attributes).

    Speed-up worth using: an attribute that is on no FD's right side must be in every key;
    an attribute that is on right sides but never on a left side is in no key."""
    schema = frozenset(schema)
    on_right = frozenset().union(*(rhs - lhs for lhs, rhs in fds)) & schema
    on_left = frozenset().union(*(lhs for lhs, _ in fds)) & schema
    core = schema - on_right
    maybe = sorted((schema & on_right & on_left))
    keys = []
    for size in range(len(maybe) + 1):
        for extra in combinations(maybe, size):
            x = core | frozenset(extra)
            if any(k <= x for k in keys):
                continue
            if is_superkey(x, schema, fds):
                keys.append(x)
    return sorted(keys, key=lambda k: (len(k), sorted(k)))


def prime_attributes(schema, fds):
    """Attributes that belong to at least one candidate key."""
    return frozenset().union(*candidate_keys(schema, fds))


def count_superkeys(schema, fds):
    """Kata: Count Them. How many superkeys does the schema have under these FDs?"""
    keys = candidate_keys(schema, fds)
    n = len(frozenset(schema))
    total = 0
    for size in range(1, len(keys) + 1):
        for chosen in combinations(keys, size):
            total += (-1) ** (size + 1) * 2 ** (n - len(frozenset().union(*chosen)))
    return total
