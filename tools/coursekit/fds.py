"""Functional dependencies in the notation exam papers use, for the normalisation days (41 to 52).

    from coursekit.fds import parse, attrs, fmt

    parse("AB->C; C->D")          [(frozenset({'A', 'B'}), frozenset({'C'})), (frozenset({'C'}), frozenset({'D'}))]
    parse("adm_no unit -> grade")  names with spaces between them work too
    attrs("ABCD")                 frozenset({'A', 'B', 'C', 'D'})
    fmt(parse("BA->C"))           'AB->C'

A side written in capital letters with no spaces is one attribute per letter ("AB" is A and B).
A side with spaces is split on the spaces ("adm_no unit"). Anything else is a single name.
FDs are separated by ";" or newlines; "->" and "→" both work.
"""

from __future__ import annotations

import re

FD = tuple  # (frozenset lhs, frozenset rhs)


def attrs(text) -> frozenset:
    """A set of attributes from "ABC", "adm_no unit", or any iterable of names."""
    if not isinstance(text, str):
        return frozenset(text)
    text = text.strip()
    if not text:
        return frozenset()
    if " " in text or "," in text:
        return frozenset(p for p in re.split(r"[\s,]+", text) if p)
    if re.fullmatch(r"[A-Z]+", text):
        return frozenset(text)
    return frozenset({text})


def parse(text: str) -> list[FD]:
    """A list of (lhs, rhs) pairs of frozensets."""
    fds = []
    for part in re.split(r"[;\n]", text):
        part = part.strip()
        if not part:
            continue
        pieces = re.split(r"->|→", part)
        if len(pieces) != 2:
            raise ValueError(f"can't read the dependency {part!r}: write it like AB->C")
        lhs, rhs = attrs(pieces[0]), attrs(pieces[1])
        if not rhs:
            raise ValueError(f"{part!r} has nothing on the right")
        fds.append((lhs, rhs))
    return fds


def _side(s) -> str:
    names = sorted(s)
    return "".join(names) if all(len(n) == 1 for n in names) else " ".join(names)


def fmt(fds) -> str:
    """'AB->C; C->D', sorted, for messages."""
    return "; ".join(sorted(f"{_side(l)}->{_side(r)}" for l, r in fds))
