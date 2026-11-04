"""Day 50: multivalued dependencies and fourth normal form.

Schemas are frozensets of attribute names. FDs and MVDs are (lhs, rhs) pairs of frozensets:
(X, Y) in `mvds` means X ->> Y. Relations are coursekit.relational.Relation values.
"""

from itertools import permutations

from coursekit.fds import attrs


def closure(attributes, fds):
    """Day 43. (Done for you.)"""
    result = set(attributes)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= result and not rhs <= result:
                result |= rhs
                changed = True
    return frozenset(result)


def _sorted_parts(parts):
    return sorted(set(parts), key=lambda p: (sorted(p), len(p)))


def holds_mvd(r, x, y):
    """Does X ->> Y hold in the relation r? x and y are anything attrs() accepts.

    For each X value, the set of (Y value, rest value) pairs must be every Y value paired with every rest
    value: Y and the rest are independent once X is fixed."""
    raise NotImplementedError("write this")


def complement(schema, x, y):
    """If X ->> Y holds in R, so does X ->> Z for the rest of the attributes. Return Z."""
    raise NotImplementedError("write this")


def is_trivial(schema, x, y):
    """X ->> Y is trivial when Y is inside X or X and Y together are the whole schema."""
    raise NotImplementedError("write this")


def violations(schema, fds, mvds):
    """The dependencies that break 4NF: non-trivial (an FD X -> Y counts as the MVD X ->> Y), and X not a
    superkey (by FD closure). A list of (X, Y) pairs, sorted by (sorted(X), sorted(Y)), no repeats."""
    raise NotImplementedError("write this")


def is_4nf(schema, fds, mvds):
    """True when nothing violates 4NF."""
    raise NotImplementedError("write this")


def decompose_4nf(schema, fds, mvds):
    """Split until every part is in 4NF. For a part P, a dependency X ->> Y (or X -> Y) applies when X is
    inside P; inside P it says X ->> (Y & P) - X (for an FD, X -> closure(X) & P). Split P on the first
    violation (sorted as in violations) into X | Y and P - (Y - X). Return the parts, sorted by
    (sorted(part), len(part))."""
    raise NotImplementedError("write this")


def mvds_in(r):
    """Kata: every single-attribute MVD {a} ->> {b} that holds in r, is non-trivial, and isn't just an FD
    (a -> b doesn't hold). A sorted list of (a, b) name pairs."""
    raise NotImplementedError("write this")
