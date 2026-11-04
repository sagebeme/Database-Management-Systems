"""Relations as sets of tuples, for the relational algebra and calculus days (36 to 38).

You wrote most of this yourself on Day 35. It's here, finished, so later days can share it:

    from coursekit.relational import Relation, make, same, show

    shows = make(["title", "channel"], [("Pwani Love", "Bahari TV"), ("Jiko Wars", "Riverwood Plus")])
    print(show(shows))
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Relation:
    """A heading (attribute names, in order) and a set of rows (tuples in heading order)."""

    heading: tuple
    rows: frozenset

    def dicts(self) -> list[dict]:
        """The tuples as dicts, sorted, for reading and for predicates."""
        return [dict(zip(self.heading, row)) for row in sorted(self.rows, key=_sort_key)]

    def __len__(self) -> int:
        return len(self.rows)


def _sort_key(row):
    return tuple((value is None, str(type(value)), value if value is not None else 0) for value in row)


def make(heading, rows) -> Relation:
    """A Relation; repeated attribute names or wrong-length rows raise ValueError. Duplicates vanish."""
    heading = tuple(heading)
    if len(set(heading)) != len(heading):
        raise ValueError(f"attribute names repeat in {heading}")
    body = set()
    for row in rows:
        row = tuple(row)
        if len(row) != len(heading):
            raise ValueError(f"{row} has {len(row)} values for {len(heading)} attributes")
        body.add(row)
    return Relation(heading, frozenset(body))


def from_dicts(heading, dicts) -> Relation:
    """A Relation from dicts (extra keys are an error)."""
    heading = tuple(heading)
    rows = []
    for d in dicts:
        if set(d) != set(heading):
            raise ValueError(f"{d} doesn't match the heading {heading}")
        rows.append(tuple(d[a] for a in heading))
    return make(heading, rows)


def same(r: Relation, s: Relation) -> bool:
    """Equal as relations: the same attribute names and tuples, whatever the attribute order."""
    if set(r.heading) != set(s.heading):
        return False
    order = [s.heading.index(a) for a in r.heading]
    return r.rows == frozenset(tuple(row[i] for i in order) for row in s.rows)


def show(r: Relation) -> str:
    """A text table, the way the mysql client draws one."""
    cells = [list(r.heading)] + [["NULL" if v is None else str(v) for v in row] for row in sorted(r.rows, key=_sort_key)]
    widths = [max(len(row[i]) for row in cells) for i in range(len(r.heading))]
    line = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    out = [line, "| " + " | ".join(h.ljust(w) for h, w in zip(cells[0], widths)) + " |", line]
    out += ["| " + " | ".join(c.ljust(w) for c, w in zip(row, widths)) + " |" for row in cells[1:]]
    out.append(line)
    return "\n".join(out)
