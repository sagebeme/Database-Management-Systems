"""Day 44: Armstrong's axioms, implied dependencies and equivalent FD sets.

An FD is a (lhs, rhs) pair of frozensets. coursekit.fds.parse("AB->C") builds a list of them.
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


def reflexivity(x, y):
    """If Y ⊆ X, then X -> Y. Return the FD (x, y); raise ValueError if y isn't inside x."""
    x, y = frozenset(x), frozenset(y)
    if not y <= x:
        raise ValueError("reflexivity needs Y inside X")
    return (x, y)


def augmentation(fd, z):
    """From X -> Y, get XZ -> YZ."""
    lhs, rhs = fd
    return (lhs | frozenset(z), rhs | frozenset(z))


def transitivity(fd1, fd2):
    """From X -> Y and Y -> Z, get X -> Z. Raise ValueError unless fd1's right side is exactly
    fd2's left side."""
    if fd1[1] != fd2[0]:
        raise ValueError("transitivity needs X -> Y and Y -> Z")
    return (fd1[0], fd2[1])


def union(fd1, fd2):
    """From X -> Y and X -> Z, get X -> YZ. Raise ValueError if the left sides differ."""
    if fd1[0] != fd2[0]:
        raise ValueError("union needs the same left side")
    return (fd1[0], fd1[1] | fd2[1])


def decomposition(fd, y):
    """From X -> YZ, get X -> Y. Raise ValueError if y isn't inside the right side."""
    y = frozenset(y)
    if not y <= fd[1]:
        raise ValueError("decomposition needs Y inside the right side")
    return (fd[0], y)


def pseudotransitivity(fd1, fd2):
    """From X -> Y and WY -> Z, get WX -> Z, where W is fd2's left side minus Y.
    Raise ValueError unless Y is inside fd2's left side."""
    x, y = fd1
    if not y <= fd2[0]:
        raise ValueError("pseudotransitivity needs X -> Y and WY -> Z")
    return ((fd2[0] - y) | x, fd2[1])


def implies(fds, fd):
    """True if the FD follows from fds (it's in F+). Use closure: X -> Y follows iff Y ⊆ X+."""
    return fd[1] <= closure(fd[0], fds)


def equivalent(f, g):
    """True if F and G imply exactly the same FDs: every FD of G follows from F, and every FD
    of F follows from G."""
    return all(implies(f, fd) for fd in g) and all(implies(g, fd) for fd in f)


def redundant(fds):
    """Kata: Spot the Spare. The FDs (in their original order) that follow from the OTHER FDs,
    each checked on its own against the rest."""
    return [fd for i, fd in enumerate(fds) if implies(fds[:i] + fds[i + 1:], fd)]
