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
    return make(r.heading, [row for row in r.rows if predicate(dict(zip(r.heading, row)))])


def project(r, attributes):
    """pi: only these attributes, in this order. Duplicates vanish (it's a set)."""
    missing = [a for a in attributes if a not in r.heading]
    if missing:
        raise ValueError(f"no attributes {missing} in {r.heading}")
    idx = [r.heading.index(a) for a in attributes]
    return make(attributes, [tuple(row[i] for i in idx) for row in r.rows])


def rename(r, mapping):
    """rho: rename attributes, {old: new}. Attributes not in mapping keep their names."""
    return make([mapping.get(a, a) for a in r.heading], r.rows)


def union(r, s):
    """r ∪ s. r and s must be union-compatible: the same attribute names (in any order),
    otherwise raise ValueError. The result uses r's attribute order."""
    return make(r.heading, r.rows | _aligned(r, s))


def difference(r, s):
    """r − s: tuples of r that aren't in s. Same compatibility rule as union."""
    return make(r.heading, r.rows - _aligned(r, s))


def product(r, s):
    """r × s: every tuple of r joined to every tuple of s. If they share an attribute name,
    raise ValueError (rename one side first)."""
    clash = set(r.heading) & set(s.heading)
    if clash:
        raise ValueError(f"both sides have {sorted(clash)}: rename first")
    return make(r.heading + s.heading, [a + b for a in r.rows for b in s.rows])


def titles_on_bahari(shows):
    """Query: π title (σ channel = 'Bahari TV' (shows)). shows is (title, channel, year)."""
    return project(select(shows, lambda t: t["channel"] == "Bahari TV"), ["title"])


def comedy_or_drama(genres):
    """Query: titles that are Comedy or Drama, as a union of two selections. genres is (title, genre)."""
    def titles(genre):
        return project(select(genres, lambda t: t["genre"] == genre), ["title"])
    return union(titles("Comedy"), titles("Drama"))


def without_genre(shows, genres):
    """Query: titles of shows that have no genre, with a difference."""
    return difference(project(shows, ["title"]), project(genres, ["title"]))


def same_channel_pairs(shows):
    """Query: pairs of different shows on the same channel: attributes (first, second), with
    first < second alphabetically. Rename two copies of shows, take their product, select, project."""
    a = rename(shows, {"title": "first", "channel": "c1", "year": "y1"})
    b = rename(shows, {"title": "second", "channel": "c2", "year": "y2"})
    both = select(product(a, b), lambda t: t["c1"] == t["c2"] and t["first"] < t["second"])
    return project(both, ["first", "second"])


def intersection(r, s):
    """Kata: Only Minus. r ∩ s, using difference and nothing else."""
    return difference(r, difference(r, s))
