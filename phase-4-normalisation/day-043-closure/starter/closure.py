"""Day 43: attribute closure, and every candidate key from a set of FDs.

FDs are (lhs, rhs) pairs of frozensets; coursekit.fds.parse("AB->C; C->D") builds them.
Attribute sets are frozensets of names.
"""

from itertools import combinations


def closure(attributes, fds):
    """X+: every attribute X determines. Start with X; while some FD's left side is inside
    what you have, add its right side. Stop when nothing changes."""
    raise NotImplementedError


def is_superkey(x, schema, fds):
    """True if x determines every attribute of schema."""
    raise NotImplementedError


def is_candidate_key(x, schema, fds):
    """A superkey none of whose proper subsets is a superkey. (Checking each subset missing
    one attribute is enough.)"""
    raise NotImplementedError


def candidate_keys(schema, fds):
    """Every candidate key, as frozensets, sorted by size and then by sorted(attributes).

    Speed-up worth using: an attribute that is on no FD's right side must be in every key;
    an attribute that is on right sides but never on a left side is in no key."""
    raise NotImplementedError


def prime_attributes(schema, fds):
    """Attributes that belong to at least one candidate key."""
    raise NotImplementedError


def count_superkeys(schema, fds):
    """Kata: Count Them. How many superkeys does the schema have under these FDs?"""
    raise NotImplementedError
