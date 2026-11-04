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
    x = sorted(attrs(x))
    y = sorted(attrs(y) - set(x))
    rest = sorted(set(r.heading) - set(x) - set(y))
    groups = {}
    for row in r.dicts():
        key = tuple(row[a] for a in x)
        groups.setdefault(key, set()).add((tuple(row[a] for a in y), tuple(row[a] for a in rest)))
    for pairs in groups.values():
        ys = {p[0] for p in pairs}
        rests = {p[1] for p in pairs}
        if len(pairs) != len(ys) * len(rests):
            return False
    return True


def complement(schema, x, y):
    """If X ->> Y holds in R, so does X ->> Z for the rest of the attributes. Return Z."""
    return frozenset(schema) - frozenset(x) - frozenset(y)


def is_trivial(schema, x, y):
    """X ->> Y is trivial when Y is inside X or X and Y together are the whole schema."""
    x, y = frozenset(x), frozenset(y)
    return y <= x or (x | y) >= frozenset(schema)


def violations(schema, fds, mvds):
    """The dependencies that break 4NF: non-trivial (an FD X -> Y counts as the MVD X ->> Y), and X not a
    superkey (by FD closure). A list of (X, Y) pairs, sorted by (sorted(X), sorted(Y)), no repeats."""
    schema = frozenset(schema)
    found = set()
    for x, y in list(fds) + list(mvds):
        if not is_trivial(schema, x, y) and not closure(x, fds) >= schema:
            found.add((frozenset(x), frozenset(y)))
    return sorted(found, key=lambda d: (sorted(d[0]), sorted(d[1])))


def is_4nf(schema, fds, mvds):
    """True when nothing violates 4NF."""
    return not violations(schema, fds, mvds)


def decompose_4nf(schema, fds, mvds):
    """Split until every part is in 4NF. For a part P, a dependency X ->> Y (or X -> Y) applies when X is
    inside P; inside P it says X ->> (Y & P) - X (for an FD, X -> closure(X) & P). Split P on the first
    violation (sorted as in violations) into X | Y and P - (Y - X). Return the parts, sorted by
    (sorted(part), len(part))."""
    parts = [frozenset(schema)]
    while True:
        for i, part in enumerate(parts):
            inside = []
            for x, y in fds:
                if x <= part:
                    inside.append((x, closure(x, fds) & part))
            for x, y in mvds:
                if x <= part:
                    inside.append((x, (y & part) - x))
            bad = sorted({(x, y) for x, y in inside
                          if y and not is_trivial(part, x, y) and not closure(x, fds) >= part},
                         key=lambda d: (sorted(d[0]), sorted(d[1])))
            if bad:
                x, y = bad[0]
                parts[i:i + 1] = [x | y, part - (y - x)]
                break
        else:
            return _sorted_parts(parts)


def mvds_in(r):
    """Kata: every single-attribute MVD {a} ->> {b} that holds in r, is non-trivial, and isn't just an FD
    (a -> b doesn't hold). A sorted list of (a, b) name pairs."""
    heading = frozenset(r.heading)
    found = []
    for a, b in permutations(sorted(heading), 2):
        if is_trivial(heading, {a}, {b}):
            continue
        values = {}
        is_fd = True
        for row in r.dicts():
            if values.setdefault(row[a], row[b]) != row[b]:
                is_fd = False
        if not is_fd and holds_mvd(r, {a}, {b}):
            found.append((a, b))
    return sorted(found)
