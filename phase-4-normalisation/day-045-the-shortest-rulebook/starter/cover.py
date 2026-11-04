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
    raise NotImplementedError


def extraneous(fd, fds):
    """The attributes of fd's left side that are extraneous, each tested on its own: a is
    extraneous if (lhs - a)+, under fds, still contains fd's right side. Return a frozenset."""
    raise NotImplementedError


def minimal_cover(fds):
    """A minimal cover of fds:
      1. split the right sides (split_right);
      2. for each FD in order, remove extraneous left attributes one at a time (smallest name
         first), re-checking after each removal, always against the current list;
      3. for each FD in order, drop it if the remaining FDs imply it."""
    raise NotImplementedError


def canonical_cover(fds):
    """The minimal cover with FDs that share a left side merged: A -> B and A -> C become A -> BC.
    Order: the order each left side first appears in the minimal cover."""
    raise NotImplementedError


def is_minimal(fds):
    """Kata: Check the Cover. True if fds is already minimal: single-attribute right sides,
    no extraneous left attribute, and no FD implied by the others."""
    raise NotImplementedError
