"""Day 45: The Shortest Rulebook. A minimal cover isn't unique, so most tests check its
properties; the examples with only one possible answer check it exactly."""

import pytest

from coursekit import load_module
from coursekit.fds import attrs, fmt, parse

CASES = [
    "A->BC; B->C; A->B; AB->C",
    "AB->C; A->B",
    "A->B; B->A; A->C; B->C",
    "ABCD->E; E->D; A->B; AC->D",
    "A->BCD; BC->DE; B->D; D->A",
    "AB->CD; A->E; E->C",
]


def closure(x, fds):
    result, changed = set(x), True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= result and not rhs <= result:
                result |= rhs
                changed = True
    return result


def equivalent(f, g):
    return all(r <= closure(l, f) for l, r in g) and all(r <= closure(l, g) for l, r in f)


@pytest.fixture
def cv(target):
    return load_module(target / "cover.py")


def test_split_right(cv):
    assert cv.split_right(parse("A->BC; AB->A; A->B")) == parse("A->B; A->C")


def test_extraneous(cv):
    fds = parse("AB->C; A->B")
    assert cv.extraneous(parse("AB->C")[0], fds) == attrs("B")
    assert cv.extraneous(parse("A->B")[0], fds) == frozenset()
    assert cv.extraneous(parse("AB->C")[0], parse("AB->C")) == frozenset()


@pytest.mark.parametrize("text", CASES)
def test_minimal_cover_properties(cv, text):
    f = parse(text)
    m = cv.minimal_cover(f)
    assert equivalent(f, m), f"{fmt(m)} isn't equivalent to {text}"
    assert all(len(r) == 1 for _, r in m), "one attribute on each right side"
    for i, (lhs, rhs) in enumerate(m):
        assert not (rhs <= closure(lhs, m[:i] + m[i + 1:])), f"{fmt([m[i]])} is redundant"
        for a in lhs:
            assert len(lhs) == 1 or not rhs <= closure(lhs - {a}, m), f"{a} is extraneous in {fmt([m[i]])}"


def test_unique_answers(cv):
    assert fmt(cv.minimal_cover(parse("A->BC; B->C; A->B; AB->C"))) == "A->B; B->C"
    assert fmt(cv.minimal_cover(parse("AB->C; A->B"))) == "A->B; A->C"
    assert fmt(cv.canonical_cover(parse("AB->C; A->B"))) == "A->BC"
    assert fmt(cv.canonical_cover(parse("ABCD->E; E->D; A->B; AC->D"))) == "A->B; AC->E; E->D"


def test_answers(target):
    a = load_module(target / "answers.py")
    assert (a.FDS_IN_THE_MINIMAL_COVER_OF_F, a.FDS_IN_THE_CANONICAL_COVER_OF_F) == (2, 2)
    assert a.EXTRANEOUS_ATTRIBUTE_IN_AB_TO_C == "B"
    assert [a.A_MINIMAL_COVER_IS_ALWAYS_UNIQUE, a.A_MINIMAL_COVER_IS_EQUIVALENT_TO_F,
            a.REMOVE_REDUNDANT_FDS_BEFORE_EXTRANEOUS_ATTRIBUTES] == [False, True, False]


def test_kata_check_the_cover(cv):
    assert cv.is_minimal(parse("A->B; B->C"))
    assert not cv.is_minimal(parse("A->BC")), "two attributes on the right"
    assert not cv.is_minimal(parse("A->B; B->C; A->C")), "A->C is redundant"
    assert not cv.is_minimal(parse("AB->C; A->B")), "B is extraneous"
    for text in CASES:
        assert cv.is_minimal(cv.minimal_cover(parse(text)))
