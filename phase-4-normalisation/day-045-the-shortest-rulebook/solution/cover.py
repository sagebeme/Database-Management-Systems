"""Day 45: minimal and canonical covers.

An FD is a (lhs, rhs) pair of frozensets; a set of FDs is a list of them.
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


def split_right(fds):
    """Step 1: one attribute on every right side. A -> BC becomes A -> B and A -> C.
    Drop exact duplicates and trivial FDs (like AB -> A). Keep the order: FD by FD, then the
    right-side attributes in sorted order."""
    out = []
    for lhs, rhs in fds:
        for a in sorted(rhs):
            fd = (lhs, frozenset({a}))
            if a not in lhs and fd not in out:
                out.append(fd)
    return out


def extraneous(fd, fds):
    """The attributes of fd's left side that are extraneous, each tested on its own: a is
    extraneous if (lhs - a)+, under fds, still contains fd's right side. Return a frozenset."""
    lhs, rhs = fd
    if len(lhs) < 2:
        return frozenset()
    return frozenset(a for a in lhs if rhs <= closure(lhs - {a}, fds))


def minimal_cover(fds):
    """A minimal cover of fds:
      1. split the right sides (split_right);
      2. for each FD in order, remove extraneous left attributes one at a time (smallest name
         first), re-checking after each removal, always against the current list;
      3. for each FD in order, drop it if the remaining FDs imply it."""
    current = split_right(fds)
    for i in range(len(current)):
        lhs, rhs = current[i]
        for a in sorted(lhs):
            if len(lhs) > 1 and rhs <= closure(lhs - {a}, current):
                lhs = lhs - {a}
                current[i] = (lhs, rhs)
    deduped = []
    for fd in current:
        if fd not in deduped:
            deduped.append(fd)
    result = list(deduped)
    for fd in deduped:
        rest = [g for g in result if g != fd]
        if fd[1] <= closure(fd[0], rest):
            result = rest
    return result


def canonical_cover(fds):
    """The minimal cover with FDs that share a left side merged: A -> B and A -> C become A -> BC.
    Order: the order each left side first appears in the minimal cover."""
    merged = {}
    for lhs, rhs in minimal_cover(fds):
        merged[lhs] = merged.get(lhs, frozenset()) | rhs
    return list(merged.items())


def is_minimal(fds):
    """Kata: Check the Cover. True if fds is already minimal: single-attribute right sides,
    no extraneous left attribute, and no FD implied by the others."""
    if any(len(rhs) != 1 for _, rhs in fds):
        return False
    if any(extraneous(fd, fds) for fd in fds):
        return False
    return not any(fd[1] <= closure(fd[0], fds[:i] + fds[i + 1:]) for i, fd in enumerate(fds))
