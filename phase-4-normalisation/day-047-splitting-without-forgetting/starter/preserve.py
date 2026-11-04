"""Day 47: dependency-preserving decomposition.

Parts and attribute sets are frozensets; FDs are (lhs, rhs) pairs of frozensets.
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


def preserved(fd, parts, fds):
    """True if fd can be checked using the parts' own FDs, without joining them.

    The fast test: Z = fd's left side. Repeat until Z stops growing: for each part Ri,
    add ((Z ∩ Ri)+ ∩ Ri) to Z, where + is closure under ALL of fds. fd is preserved if its
    right side ends up inside Z."""
    raise NotImplementedError


def is_dependency_preserving(parts, fds):
    """True if every FD in fds is preserved."""
    raise NotImplementedError


def lost(parts, fds):
    """The FDs of fds that are not preserved, in their original order."""
    raise NotImplementedError


def project_fds(fds, part):
    """Kata: What Each Table Knows. The FDs that hold inside one part: for every non-empty
    subset X of part (smallest first, in sorted order), X -> (X+ ∩ part) - X, when that is
    non-empty. Skip an X if a smaller subset of it already determines everything it would."""
    raise NotImplementedError
