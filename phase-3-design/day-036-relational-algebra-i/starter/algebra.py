"""Day 36: relational algebra I, the six basic operators, and queries built from them.

Every operator takes relations and returns a NEW relation; nothing is changed in place.
"""

from coursekit.relational import Relation, make


def _aligned(r, s):
    """s's rows reordered to r's heading. (Done for you.)"""
    if set(r.heading) != set(s.heading):
        raise ValueError(f"not union-compatible: {r.heading} and {s.heading}")
    order = [s.heading.index(a) for a in r.heading]
    return frozenset(tuple(row[i] for i in order) for row in s.rows)


def select(r, predicate):
    """sigma: the tuples of r for which predicate(row) is true. row is a dict {attribute: value}."""
    raise NotImplementedError


def project(r, attributes):
    """pi: only these attributes, in this order. Duplicates vanish (it's a set)."""
    raise NotImplementedError


def rename(r, mapping):
    """rho: rename attributes, {old: new}. Attributes not in mapping keep their names."""
    raise NotImplementedError


def union(r, s):
    """r ∪ s. r and s must be union-compatible: the same attribute names (in any order),
    otherwise raise ValueError. The result uses r's attribute order."""
    raise NotImplementedError


def difference(r, s):
    """r − s: tuples of r that aren't in s. Same compatibility rule as union."""
    raise NotImplementedError


def product(r, s):
    """r × s: every tuple of r joined to every tuple of s. If they share an attribute name,
    raise ValueError (rename one side first)."""
    raise NotImplementedError


def titles_on_bahari(shows):
    """Query: π title (σ channel = 'Bahari TV' (shows)). shows is (title, channel, year)."""
    raise NotImplementedError


def comedy_or_drama(genres):
    """Query: titles that are Comedy or Drama, as a union of two selections. genres is (title, genre)."""
    raise NotImplementedError


def without_genre(shows, genres):
    """Query: titles of shows that have no genre, with a difference."""
    raise NotImplementedError


def same_channel_pairs(shows):
    """Query: pairs of different shows on the same channel: attributes (first, second), with
    first < second alphabetically. Rename two copies of shows, take their product, select, project."""
    raise NotImplementedError


def intersection(r, s):
    """Kata: Only Minus. r ∩ s, using difference and nothing else."""
    raise NotImplementedError
