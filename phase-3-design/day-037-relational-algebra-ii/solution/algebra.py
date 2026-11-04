"""Day 37: relational algebra II: joins and division."""

from coursekit.relational import make


def natural_join(r, s):
    """r ⋈ s: pair tuples that agree on every attribute the two share. The result has r's
    attributes, then s's attributes that r doesn't have. With nothing shared, it's r × s."""
    common = [a for a in r.heading if a in s.heading]
    extra = [a for a in s.heading if a not in r.heading]
    ri, si = [r.heading.index(a) for a in common], [s.heading.index(a) for a in common]
    xi = [s.heading.index(a) for a in extra]
    rows = [a + tuple(b[i] for i in xi) for a in r.rows for b in s.rows
            if tuple(a[i] for i in ri) == tuple(b[i] for i in si)]
    return make(r.heading + tuple(extra), rows)


def theta_join(r, s, predicate):
    """r ⋈θ s: pairs of tuples (attribute names must all differ) for which predicate(row)
    is true, where row is a dict of all the attributes."""
    if set(r.heading) & set(s.heading):
        raise ValueError("rename first: the attribute names clash")
    heading = r.heading + s.heading
    return make(heading, [a + b for a in r.rows for b in s.rows if predicate(dict(zip(heading, a + b)))])


def left_outer_join(r, s):
    """r ⟕ s: the natural join, plus every tuple of r with no match, padded with None."""
    joined = natural_join(r, s)
    matched = {row[:len(r.heading)] for row in joined.rows}
    pad = (None,) * (len(joined.heading) - len(r.heading))
    return make(joined.heading, set(joined.rows) | {row + pad for row in r.rows if row not in matched})


def semi_join(r, s):
    """r ⋉ s: the tuples of r that match at least one tuple of s (on the shared attributes).
    The result has r's heading."""
    joined = natural_join(r, s)
    return make(r.heading, {row[:len(r.heading)] for row in joined.rows})


def divide(r, s):
    """r ÷ s. s's attributes are a subset of r's. Return the values of r's OTHER attributes
    (in r's order) that appear in r together with EVERY tuple of s."""
    keep = [a for a in r.heading if a not in s.heading]
    ki = [r.heading.index(a) for a in keep]
    si = [r.heading.index(a) for a in s.heading]
    pairs = {(tuple(row[i] for i in ki), tuple(row[i] for i in si)) for row in r.rows}
    candidates = {k for k, _ in pairs}
    return make(keep, [k for k in candidates if all((k, t) in pairs for t in s.rows)])


def divide_with_basics(r, s):
    """Kata: Division the Hard Way. The same answer as divide, built only from projection,
    product and difference: π_A(r) − π_A((π_A(r) × s) − r), where A is r's other attributes.
    Use the helpers _project, _product and _minus below."""
    keep = [a for a in r.heading if a not in s.heading]
    a = _project(r, keep)
    every_pair = _product(a, s)
    missing = _minus(every_pair, _project(r, list(every_pair.heading)))
    return _minus(a, _project(missing, keep))


# Day 36's operators, finished, for the kata.
def _project(r, attributes):
    idx = [r.heading.index(a) for a in attributes]
    return make(attributes, [tuple(row[i] for i in idx) for row in r.rows])


def _product(r, s):
    return make(r.heading + s.heading, [a + b for a in r.rows for b in s.rows])


def _minus(r, s):
    order = [s.heading.index(a) for a in r.heading]
    return make(r.heading, r.rows - {tuple(row[i] for i in order) for row in s.rows})
