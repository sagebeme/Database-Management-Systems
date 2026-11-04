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
    raise NotImplementedError


def augmentation(fd, z):
    """From X -> Y, get XZ -> YZ."""
    raise NotImplementedError


def transitivity(fd1, fd2):
    """From X -> Y and Y -> Z, get X -> Z. Raise ValueError unless fd1's right side is exactly
    fd2's left side."""
    raise NotImplementedError


def union(fd1, fd2):
    """From X -> Y and X -> Z, get X -> YZ. Raise ValueError if the left sides differ."""
    raise NotImplementedError


def decomposition(fd, y):
    """From X -> YZ, get X -> Y. Raise ValueError if y isn't inside the right side."""
    raise NotImplementedError


def pseudotransitivity(fd1, fd2):
    """From X -> Y and WY -> Z, get WX -> Z, where W is fd2's left side minus Y.
    Raise ValueError unless Y is inside fd2's left side."""
    raise NotImplementedError


def implies(fds, fd):
    """True if the FD follows from fds (it's in F+). Use closure: X -> Y follows iff Y ⊆ X+."""
    raise NotImplementedError


def equivalent(f, g):
    """True if F and G imply exactly the same FDs: every FD of G follows from F, and every FD
    of F follows from G."""
    raise NotImplementedError


def redundant(fds):
    """Kata: Spot the Spare. The FDs (in their original order) that follow from the OTHER FDs,
    each checked on its own against the rest."""
    raise NotImplementedError
