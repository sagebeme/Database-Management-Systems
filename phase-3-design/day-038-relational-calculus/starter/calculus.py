"""Day 38: relational calculus, written as Python comprehensions.

Each relation arrives as a list of dicts (tuple calculus: t["title"] is t.title) except in the
domain-calculus question, which gets plain tuples. Return a set of titles (strings) unless the
docstring says otherwise.

    ∃ x ∈ R (P)   ->  any(P for x in R)
    ∀ x ∈ R (P)   ->  all(P for x in R)
    P → Q         ->  (not P) or Q
"""


def recent(shows):
    """{ t.title | t ∈ SHOWS ∧ t.year ≥ 2020 }"""
    raise NotImplementedError


def has_drama(shows, genres):
    """{ s.title | s ∈ SHOWS ∧ ∃ g ∈ GENRES (g.title = s.title ∧ g.genre = 'Drama') }"""
    raise NotImplementedError


def no_genre(shows, genres):
    """{ s.title | s ∈ SHOWS ∧ ¬∃ g ∈ GENRES (g.title = s.title) }"""
    raise NotImplementedError


def never_below_seven(shows, ratings):
    """{ s.title | s ∈ SHOWS ∧ ∀ r ∈ RATINGS (r.title = s.title → r.rate ≥ 7) }

    Read it carefully: a show with no ratings at all satisfies it."""
    raise NotImplementedError


def never_below_seven_and_rated(shows, ratings):
    """The same, but only shows with at least one rating: add ∃ r ∈ RATINGS (r.title = s.title)."""
    raise NotImplementedError


def bahari_years(shows):
    """Domain calculus. shows is a list of tuples (title, channel, year).
    { ⟨y⟩ | ∃ t, c ( ⟨t, c, y⟩ ∈ SHOWS ∧ c = 'Bahari TV' ) }  -> a set of years (ints)."""
    raise NotImplementedError


def every_core_unit(registrations, core):
    """Kata: Every, Without Division. registrations has dicts {adm_no, code}; core has dicts {code}.
    { a | ∃ r ∈ REG (r.adm_no = a) ∧ ∀ u ∈ CORE ∃ r ∈ REG (r.adm_no = a ∧ r.code = u.code) }
    Return the set of adm_no values."""
    raise NotImplementedError
