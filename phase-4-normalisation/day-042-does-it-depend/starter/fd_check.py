"""Day 42: functional dependencies, checked against rows (dicts)."""

from itertools import combinations


def is_trivial(lhs, rhs):
    """True if lhs -> rhs is trivial: everything on the right is already on the left."""
    raise NotImplementedError


def holds(rows, lhs, rhs):
    """True if lhs -> rhs holds in these rows: any two rows that agree on every lhs attribute
    also agree on every rhs attribute."""
    raise NotImplementedError


def violations(rows, lhs, rhs):
    """The lhs values (as tuples, sorted) that appear with more than one rhs value."""
    raise NotImplementedError


def holding_fds(rows, attributes):
    """Kata: Find Them All. Every non-trivial FD X -> A that holds in the rows, where A is one
    attribute, X has one or two attributes, and X is minimal (no smaller part of X already
    determines A). Return (tuple of X in attributes order, A) pairs, sorted."""
    raise NotImplementedError
