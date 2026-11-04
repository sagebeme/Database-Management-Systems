"""Day 46: lossless-join decomposition.

A schema or a part is a frozenset of attribute names; FDs are (lhs, rhs) pairs of frozensets.
"""


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


def binary_lossless(r1, r2, fds):
    """Splitting into two parts is lossless exactly when the common attributes determine all of
    r1 or all of r2: (r1 ∩ r2)+ contains r1, or contains r2."""
    raise NotImplementedError


def chase(schema, parts, fds):
    """The tableau ("chase") test for any number of parts.

    Make one row per part. In the column of attribute A, a row holds "a" (distinguished) if
    its part contains A, otherwise its own symbol, like ("b", row, A). Then repeat until nothing
    changes: for each FD X -> Y, rows that agree on every X column must agree on every Y
    column, so make them equal, preferring "a" when one of them has it (otherwise take any
    one of their symbols). The split is lossless if some row ends up all "a"."""
    raise NotImplementedError


def spurious(rows, parts):
    """Kata: Count the Ghosts. rows are dicts (a relation's tuples). Project them onto each part,
    natural-join the projections back together, and return the joined rows (dicts) that were
    NOT in the original, sorted by their values in sorted-attribute order."""
    raise NotImplementedError
