"""Day 35: a relation is a set of tuples over a heading of attribute names."""

from dataclasses import dataclass
from math import prod


@dataclass(frozen=True)
class Relation:
    """A heading (attribute names, in order) and a set of rows (tuples in heading order). (Done for you.)"""
    heading: tuple
    rows: frozenset


def make(heading, rows):
    """A Relation from a heading and any iterable of rows (lists or tuples).

    Raise ValueError if two attributes share a name, or if a row's length doesn't match the
    heading. Duplicate rows simply disappear: a relation is a set."""
    raise NotImplementedError


def degree(r):
    """The number of attributes."""
    raise NotImplementedError


def cardinality(r):
    """The number of tuples."""
    raise NotImplementedError


def same(r, s):
    """True if r and s are the same relation. Attributes are known by name, so their order in
    the heading doesn't matter: (name, county) with ('Molo', 'Nakuru') equals (county, name)
    with ('Nakuru', 'Molo')."""
    raise NotImplementedError


def in_domains(r, domains):
    """True if every value is in its attribute's domain. domains maps each attribute name to
    the set of values it may take."""
    raise NotImplementedError


def from_result(result):
    """A Relation from a coursekit Result (what the tests get back from MySQL): its columns
    are the heading, its rows the tuples."""
    raise NotImplementedError


def possible_tuples(domain_sizes):
    """Kata: How Many Relations? With these domain sizes (one per attribute), how many
    different tuples could exist?"""
    raise NotImplementedError


def possible_relations(domain_sizes):
    """Kata: ...and how many different relation instances (sets of those tuples, the empty
    set included)?"""
    raise NotImplementedError
