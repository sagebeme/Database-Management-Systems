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
    common = closure(frozenset(r1) & frozenset(r2), fds)
    return frozenset(r1) <= common or frozenset(r2) <= common


def chase(schema, parts, fds):
    """The tableau ("chase") test for any number of parts.

    Make one row per part. In the column of attribute A, a row holds "a" (distinguished) if
    its part contains A, otherwise its own symbol, like ("b", row, A). Then repeat until nothing
    changes: for each FD X -> Y, rows that agree on every X column must agree on every Y
    column, so make them equal, preferring "a" when one of them has it (otherwise take any
    one of their symbols). The split is lossless if some row ends up all "a"."""
    schema = sorted(schema)
    rows = [{a: ("a" if a in part else ("b", i, a)) for a in schema} for i, part in enumerate(parts)]
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            groups = {}
            for row in rows:
                groups.setdefault(tuple(row[a] for a in sorted(lhs)), []).append(row)
            for group in groups.values():
                if len(group) < 2:
                    continue
                for a in rhs:
                    values = {row[a] for row in group}
                    if len(values) > 1:
                        keep = "a" if "a" in values else min(values, key=repr)
                        for row in rows:
                            if row[a] in values and row[a] != keep:
                                row[a] = keep
                        changed = True
    return any(all(row[a] == "a" for a in schema) for row in rows)


def spurious(rows, parts):
    """Kata: Count the Ghosts. rows are dicts (a relation's tuples). Project them onto each part,
    natural-join the projections back together, and return the joined rows (dicts) that were
    NOT in the original, sorted by their values in sorted-attribute order."""
    def project(rs, attrs):
        return {tuple(sorted((a, r[a]) for a in attrs)) for r in rs}
    joined = [dict(t) for t in project(rows, parts[0])]
    for part in parts[1:]:
        right = [dict(t) for t in project(rows, part)]
        joined = [{**l, **r} for l in joined for r in right
                  if all(l[a] == r[a] for a in set(l) & set(r))]
    original = {tuple(sorted(r.items())) for r in rows}
    ghosts = {tuple(sorted(j.items())) for j in joined} - original
    return [dict(g) for g in sorted(ghosts, key=lambda g: [v for _, v in g])]
