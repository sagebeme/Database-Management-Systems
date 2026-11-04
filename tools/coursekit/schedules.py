"""Schedules in the notation exam papers use, for the transaction days (66 to 73).

    from coursekit.schedules import parse, fmt

    parse("r1(A) w2(A) c1 a2")
    [Op('r', 1, 'A'), Op('w', 2, 'A'), Op('c', 1, None), Op('a', 2, None)]

Operations, separated by spaces, commas or semicolons:

    r1(A)   T1 reads A            c1   T1 commits
    w1(A)   T1 writes A           a1   T1 aborts
    sl1(A)  T1 takes a shared lock on A        (Day 71)
    xl1(A)  T1 takes an exclusive lock on A    (Day 71)
    u1(A)   T1 unlocks A                       (Day 71)
"""

from __future__ import annotations

import re
from typing import NamedTuple

_OP = re.compile(r"(sl|xl|r|w|u)(\d+)\(\s*(\w+)\s*\)|(c|a)(\d+)")


class Op(NamedTuple):
    kind: str          # 'r', 'w', 'c', 'a', 'sl', 'xl' or 'u'
    txn: int
    item: str | None   # None for commits and aborts


def parse(text: str) -> list[Op]:
    """The operations in order. Anything that isn't an operation (or a separator) raises ValueError."""
    ops, pos = [], 0
    text = text.strip()
    while pos < len(text):
        if text[pos] in " \t\n,;":
            pos += 1
            continue
        m = _OP.match(text, pos)
        if not m:
            raise ValueError(f"can't read the schedule at {text[pos:pos + 12]!r}: write operations like r1(A) w2(B) c1")
        if m.group(1):
            ops.append(Op(m.group(1), int(m.group(2)), m.group(3)))
        else:
            ops.append(Op(m.group(4), int(m.group(5)), None))
        pos = m.end()
    return ops


def fmt(ops) -> str:
    """Back to text: 'r1(A) w2(A) c1'."""
    return " ".join(f"{o.kind}{o.txn}" if o.item is None else f"{o.kind}{o.txn}({o.item})" for o in ops)


def transactions(ops) -> list[int]:
    """The transaction numbers in the schedule, sorted."""
    return sorted({o.txn for o in ops})
