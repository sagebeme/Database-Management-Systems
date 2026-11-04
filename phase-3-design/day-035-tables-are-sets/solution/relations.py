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
    heading = tuple(heading)
    if len(set(heading)) != len(heading):
        raise ValueError(f"attribute names repeat in {heading}")
    clean = set()
    for row in rows:
        row = tuple(row)
        if len(row) != len(heading):
            raise ValueError(f"{row} has {len(row)} values for {len(heading)} attributes")
        clean.add(row)
    return Relation(heading, frozenset(clean))


def degree(r):
    """The number of attributes."""
    return len(r.heading)


def cardinality(r):
    """The number of tuples."""
    return len(r.rows)


def same(r, s):
    """True if r and s are the same relation. Attributes are known by name, so their order in
    the heading doesn't matter: (name, county) with ('Molo', 'Nakuru') equals (county, name)
    with ('Nakuru', 'Molo')."""
    if set(r.heading) != set(s.heading):
        return False
    order = [s.heading.index(a) for a in r.heading]
    return r.rows == frozenset(tuple(row[i] for i in order) for row in s.rows)


def in_domains(r, domains):
    """True if every value is in its attribute's domain. domains maps each attribute name to
    the set of values it may take."""
    return all(row[i] in domains[a] for row in r.rows for i, a in enumerate(r.heading))


def from_result(result):
    """A Relation from a coursekit Result (what the tests get back from MySQL): its columns
    are the heading, its rows the tuples."""
    return make(result.columns, result.rows)


def possible_tuples(domain_sizes):
    """Kata: How Many Relations? With these domain sizes (one per attribute), how many
    different tuples could exist?"""
    return prod(domain_sizes)


def possible_relations(domain_sizes):
    """Kata: ...and how many different relation instances (sets of those tuples, the empty
    set included)?"""
    return 2 ** possible_tuples(domain_sizes)
