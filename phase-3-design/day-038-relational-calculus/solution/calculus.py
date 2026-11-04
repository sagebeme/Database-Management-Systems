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
    return {t["title"] for t in shows if t["year"] >= 2020}


def has_drama(shows, genres):
    """{ s.title | s ∈ SHOWS ∧ ∃ g ∈ GENRES (g.title = s.title ∧ g.genre = 'Drama') }"""
    return {s["title"] for s in shows
            if any(g["title"] == s["title"] and g["genre"] == "Drama" for g in genres)}


def no_genre(shows, genres):
    """{ s.title | s ∈ SHOWS ∧ ¬∃ g ∈ GENRES (g.title = s.title) }"""
    return {s["title"] for s in shows if not any(g["title"] == s["title"] for g in genres)}


def never_below_seven(shows, ratings):
    """{ s.title | s ∈ SHOWS ∧ ∀ r ∈ RATINGS (r.title = s.title → r.rate ≥ 7) }

    Read it carefully: a show with no ratings at all satisfies it."""
    return {s["title"] for s in shows
            if all(r["title"] != s["title"] or r["rate"] >= 7 for r in ratings)}


def never_below_seven_and_rated(shows, ratings):
    """The same, but only shows with at least one rating: add ∃ r ∈ RATINGS (r.title = s.title)."""
    return {title for title in never_below_seven(shows, ratings)
            if any(r["title"] == title for r in ratings)}


def bahari_years(shows):
    """Domain calculus. shows is a list of tuples (title, channel, year).
    { ⟨y⟩ | ∃ t, c ( ⟨t, c, y⟩ ∈ SHOWS ∧ c = 'Bahari TV' ) }  -> a set of years (ints)."""
    return {y for (t, c, y) in shows if c == "Bahari TV"}


def every_core_unit(registrations, core):
    """Kata: Every, Without Division. registrations has dicts {adm_no, code}; core has dicts {code}.
    { a | ∃ r ∈ REG (r.adm_no = a) ∧ ∀ u ∈ CORE ∃ r ∈ REG (r.adm_no = a ∧ r.code = u.code) }
    Return the set of adm_no values."""
    students = {r["adm_no"] for r in registrations}
    return {a for a in students
            if all(any(r["adm_no"] == a and r["code"] == u["code"] for r in registrations) for u in core)}
