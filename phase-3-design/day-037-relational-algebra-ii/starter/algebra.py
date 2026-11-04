"""Day 37: relational algebra II: joins and division."""

from coursekit.relational import make


def natural_join(r, s):
    """r ⋈ s: pair tuples that agree on every attribute the two share. The result has r's
    attributes, then s's attributes that r doesn't have. With nothing shared, it's r × s."""
    raise NotImplementedError


def theta_join(r, s, predicate):
    """r ⋈θ s: pairs of tuples (attribute names must all differ) for which predicate(row)
    is true, where row is a dict of all the attributes."""
    raise NotImplementedError


def left_outer_join(r, s):
    """r ⟕ s: the natural join, plus every tuple of r with no match, padded with None."""
    raise NotImplementedError


def semi_join(r, s):
    """r ⋉ s: the tuples of r that match at least one tuple of s (on the shared attributes).
    The result has r's heading."""
    raise NotImplementedError


def divide(r, s):
    """r ÷ s. s's attributes are a subset of r's. Return the values of r's OTHER attributes
    (in r's order) that appear in r together with EVERY tuple of s."""
    raise NotImplementedError


def divide_with_basics(r, s):
    """Kata: Division the Hard Way. The same answer as divide, built only from projection,
    product and difference: π_A(r) − π_A((π_A(r) × s) − r), where A is r's other attributes.
    Use the helpers _project, _product and _minus below."""
    raise NotImplementedError


# Day 36's operators, finished, for the kata.
def _project(r, attributes):
    idx = [r.heading.index(a) for a in attributes]
    return make(attributes, [tuple(row[i] for i in idx) for row in r.rows])


def _product(r, s):
    return make(r.heading + s.heading, [a + b for a in r.rows for b in s.rows])


def _minus(r, s):
    order = [s.heading.index(a) for a in r.heading]
    return make(r.heading, r.rows - {tuple(row[i] for i in order) for row in s.rows})
