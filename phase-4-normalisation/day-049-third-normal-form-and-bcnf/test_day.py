"""Day 49: Third Normal Form and BCNF. Decompositions aren't unique, so the tests check what a
correct one must be: lossless, in the target normal form, and (for 3NF) dependency preserving."""

from itertools import combinations

import pytest

from coursekit import load_module
from coursekit.fds import attrs, parse

CASES = [  # (schema, FDs, highest normal form)
    ("ABC", "A->B; B->C", "2NF"),
    ("ABC", "AB->C; C->B", "3NF"),
    ("ABCD", "AB->CD; A->C", "1NF"),
    ("AB", "A->B", "BCNF"),
    ("ABCDE", "A->B; BC->E; ED->A", "3NF"),
    ("student course tutor", "student course -> tutor; tutor -> course", "3NF"),
    ("ABCDEF", "AB->C; C->D; D->E; E->F", "2NF"),
    ("ABCDEFGH", "A->BC; C->D; E->F; G->H", "1NF"),
    ("ABCD", "A->BCD; B->A", "BCNF"),
]


def closure(x, fds):
    result, changed = set(x), True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= result and not rhs <= result:
                result |= rhs
                changed = True
    return frozenset(result)


def part_is_bcnf(part, fds):
    for size in range(1, len(part)):
        for x in combinations(sorted(part), size):
            plus = closure(x, fds) & part
            if plus != frozenset(x) and plus != part:
                return False
    return True


def lossless(schema, parts, fds):
    schema = sorted(schema)
    rows = [{a: ("a" if a in p else ("b", i, a)) for a in schema} for i, p in enumerate(parts)]
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            groups = {}
            for row in rows:
                groups.setdefault(tuple(row[a] for a in sorted(lhs)), []).append(row)
            for group in groups.values():
                for a in rhs:
                    values = {row[a] for row in group}
                    if len(values) > 1:
                        keep = "a" if "a" in values else min(values, key=repr)
                        for row in rows:
                            if row[a] in values and row[a] != keep:
                                row[a] = keep
                        changed = True
    return any(all(row[a] == "a" for a in schema) for row in rows)


def preserving(parts, fds):
    for lhs, rhs in fds:
        z, grew = set(lhs), True
        while grew:
            grew = False
            for p in parts:
                gained = (closure(z & p, fds) & p) - z
                if gained:
                    z |= gained
                    grew = True
        if not rhs <= z:
            return False
    return True


@pytest.fixture
def nf(target):
    return load_module(target / "normal_forms.py")


@pytest.mark.parametrize("schema, fds, highest", CASES)
def test_is_3nf_and_is_bcnf(nf, schema, fds, highest):
    s, f = attrs(schema), parse(fds)
    assert nf.is_bcnf(s, f) is (highest == "BCNF")
    assert nf.is_3nf(s, f) is (highest in ("3NF", "BCNF"))


@pytest.mark.parametrize("schema, fds, highest", CASES)
def test_bcnf_decompose(nf, schema, fds, highest):
    s, f = attrs(schema), parse(fds)
    parts = nf.bcnf_decompose(s, f)
    assert frozenset().union(*parts) == s, "every attribute lands in some part"
    assert all(part_is_bcnf(p, f) for p in parts), "every part in BCNF"
    assert lossless(s, parts, f), "and the split is lossless"
    if highest == "BCNF":
        assert parts == [s], "already in BCNF: don't split"


@pytest.mark.parametrize("schema, fds, highest", CASES)
def test_synthesize_3nf(nf, schema, fds, highest):
    s, f = attrs(schema), parse(fds)
    parts = nf.synthesize_3nf(s, f)
    assert frozenset().union(*parts) == s
    assert lossless(s, parts, f)
    assert preserving(parts, f), "3NF synthesis keeps every FD checkable"
    assert not any(p < q for p in parts for q in parts), "no part inside another"


def test_the_classic_trade(nf):
    s, f = attrs("student course tutor"), parse("student course -> tutor; tutor -> course")
    assert nf.synthesize_3nf(s, f) == [s], "already in 3NF: one table"
    parts = nf.bcnf_decompose(s, f)
    assert not preserving(parts, f), "BCNF here must lose student course -> tutor"


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.R1, a.R2, a.R3, a.R4, a.R5] == ["2NF", "3NF", "1NF", "BCNF", "3NF"]
    assert [a.EVERY_BCNF_RELATION_IS_IN_3NF, a.EVERY_TWO_ATTRIBUTE_RELATION_IS_IN_BCNF,
            a.BCNF_DECOMPOSITION_ALWAYS_PRESERVES_DEPENDENCIES,
            a.THREE_NF_SYNTHESIS_ALWAYS_PRESERVES_DEPENDENCIES] == [True, True, False, True]


@pytest.mark.parametrize("schema, fds, highest", CASES)
def test_kata_how_normal_is_it(nf, schema, fds, highest):
    assert nf.highest_normal_form(attrs(schema), parse(fds)) == highest
