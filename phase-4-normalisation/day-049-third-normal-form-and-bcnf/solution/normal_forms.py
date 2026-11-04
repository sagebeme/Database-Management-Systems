"""Day 49: third normal form and BCNF.

Schemas and parts are frozensets of attribute names; FDs are (lhs, rhs) pairs of frozensets.
"""

from itertools import combinations


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


def candidate_keys(schema, fds):
    """Day 43. (Done for you.)"""
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


def minimal_cover(fds):
    """Day 45. (Done for you.)"""
    current = []
    for lhs, rhs in fds:
        for a in sorted(rhs):
            fd = (lhs, frozenset({a}))
            if a not in lhs and fd not in current:
                current.append(fd)
    for i in range(len(current)):
        lhs, rhs = current[i]
        for a in sorted(lhs):
            if len(lhs) > 1 and rhs <= closure(lhs - {a}, current):
                lhs = lhs - {a}
                current[i] = (lhs, rhs)
    result = []
    for fd in current:
        if fd not in result:
            result.append(fd)
    for fd in list(result):
        rest = [g for g in result if g != fd]
        if fd[1] <= closure(fd[0], rest):
            result = rest
    return result


def _sorted_parts(parts):
    return sorted(set(parts), key=lambda p: (sorted(p), len(p)))


def is_3nf(schema, fds):
    """3NF: for every non-trivial X -> A in fds (one attribute A at a time), X is a superkey
    OR A is prime."""
    schema = frozenset(schema)
    prime = frozenset().union(*candidate_keys(schema, fds))
    for lhs, rhs in fds:
        for a in rhs - lhs:
            if not closure(lhs, fds) >= schema and a not in prime:
                return False
    return True


def is_bcnf(schema, fds):
    """BCNF: for every non-trivial X -> Y in fds, X is a superkey."""
    schema = frozenset(schema)
    return all(rhs <= lhs or closure(lhs, fds) >= schema for lhs, rhs in fds)


def bcnf_decompose(schema, fds):
    """Split until every part is in BCNF. For a part R, look for a violation: a subset X of R
    (smallest first, sorted) whose closure (under ALL fds) adds attributes of R, but doesn't
    cover R. Split R into (X+ ∩ R) and (R - (X+ - X)), and keep going on both.
    Return the parts sorted with _sorted_parts."""
    todo, done = [frozenset(schema)], []
    while todo:
        part = todo.pop()
        for size in range(1, len(part)):
            hit = None
            for x in combinations(sorted(part), size):
                x = frozenset(x)
                plus = closure(x, fds) & part
                if plus != x and plus != part:
                    hit = (x, plus)
                    break
            if hit:
                x, plus = hit
                todo += [plus, part - (plus - x)]
                break
        else:
            done.append(part)
    return _sorted_parts(done)


def synthesize_3nf(schema, fds):
    """The 3NF synthesis algorithm (lossless and dependency preserving):
      1. take a minimal cover, and merge FDs with the same left side;
      2. make a part X ∪ Y for each X -> Y;
      3. if no part contains a candidate key, add one (the first from candidate_keys);
      4. drop any part contained in another.
    Return the parts sorted with _sorted_parts."""
    merged = {}
    for lhs, rhs in minimal_cover(fds):
        merged[lhs] = merged.get(lhs, frozenset()) | rhs
    parts = [lhs | rhs for lhs, rhs in merged.items()]
    keys = candidate_keys(schema, fds)
    if not any(any(k <= p for k in keys) for p in parts):
        parts.append(keys[0])
    parts = [p for p in parts if not any(p < q for q in parts)]
    return _sorted_parts(parts)


def highest_normal_form(schema, fds):
    """Kata: How Normal Is It? "BCNF", "3NF", "2NF" or "1NF" (assume the relation is in 1NF).
    2NF fails when a non-prime attribute depends on a proper subset of a candidate key."""
    if is_bcnf(schema, fds):
        return "BCNF"
    if is_3nf(schema, fds):
        return "3NF"
    keys = candidate_keys(schema, fds)
    prime = frozenset().union(*keys)
    for key in keys:
        for size in range(1, len(key)):
            for x in combinations(sorted(key), size):
                if (closure(frozenset(x), fds) - prime - frozenset(x)):
                    return "1NF"
    return "2NF"
