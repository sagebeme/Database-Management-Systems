"""Day 70: View Serializability."""

from collections import Counter

import pytest

from coursekit import load_module
from coursekit.schedules import parse


@pytest.fixture
def v(target):
    return load_module(target / "view.py")


def test_reads(v):
    assert v.reads(parse("r1(A) w2(A) w1(A) w3(A) r4(A)")) == Counter({(1, None, "A"): 1, (4, 3, "A"): 1})
    assert v.reads(parse("w1(A) r1(A) r2(A) r2(A)")) == Counter({(1, 1, "A"): 1, (2, 1, "A"): 2}), \
        "reading your own write counts, and so does reading twice"
    assert v.reads(parse("w1(B) r2(A) c1 r3(B)")) == Counter({(2, None, "A"): 1, (3, 1, "B"): 1})


def test_final_writes(v):
    assert v.final_writes(parse("w1(A) w2(B) w3(A) r1(B)")) == {"A": 3, "B": 2}
    assert v.final_writes(parse("r1(A) r2(A)")) == {}


@pytest.mark.parametrize("s1, s2, same", [
    ("r1(A) w2(A) w1(A) w3(A)", "r1(A) w1(A) w2(A) w3(A)", True),
    ("r1(A) w2(A) w1(A)", "r1(A) w1(A) w2(A)", False),
    ("r1(A) w1(A) r2(A) w2(A)", "r1(A) r2(A) w1(A) w2(A)", False),
    ("r1(A) w1(B) c1 r2(B)", "r1(A) w1(B) r2(B)", True),
    ("r1(A) w1(A)", "r1(A) w1(B)", False),
])
def test_view_equivalent(v, s1, s2, same):
    assert v.view_equivalent(parse(s1), parse(s2)) is same


@pytest.mark.parametrize("schedule, want", [
    ("r1(A) w2(A) w1(A) w3(A)", True),
    ("r1(A) w2(A) w1(A)", False),
    ("r1(A) w1(A) r2(A) w2(A)", True),
    ("r1(A) r2(A) w1(A) w2(A)", False),
    ("r1(A) w2(A) w1(A) w3(A) r4(A)", True),
    ("w1(A) w2(A) w2(B) w1(B) w3(B)", True),
    ("w1(A) w2(A) w2(B) w1(B)", False),
])
def test_is_view_serializable(v, schedule, want):
    assert v.is_view_serializable(parse(schedule)) is want


def test_blind_writes(v):
    assert v.blind_writes(parse("r1(A) w2(A) w1(A) w3(A)")) == [(2, "A"), (3, "A")]
    assert v.blind_writes(parse("r1(A) w1(A) w1(A) w2(B) r2(B) w2(B)")) == [(2, "B")], "each (txn, item) once"


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.EVERY_CONFLICT_SERIALIZABLE_SCHEDULE_IS_VIEW_SERIALIZABLE,
            a.EVERY_VIEW_SERIALIZABLE_SCHEDULE_IS_CONFLICT_SERIALIZABLE,
            a.VIEW_BUT_NOT_CONFLICT_SERIALIZABLE_NEEDS_A_BLIND_WRITE,
            a.CHECKING_VIEW_SERIALIZABILITY_IS_AS_CHEAP_AS_CHECKING_FOR_A_CYCLE] == [True, False, True, False]


@pytest.mark.parametrize("schedule, want", [
    ("r1(A) w1(A) r2(A) w2(A)", "conflict serializable"),
    ("r1(A) w2(A) w1(A) w3(A)", "view serializable only"),
    ("w1(A) w2(A) w2(B) w1(B) w3(B)", "view serializable only"),
    ("r1(A) w2(A) w1(A)", "not serializable"),
    ("r2(A) r1(A) w1(C) r3(C) w1(B) r4(B) w3(A) r4(C) w2(D) r2(B) w4(A) w4(B)", "conflict serializable"),
])
def test_kata_explain(v, schedule, want):
    assert v.explain(parse(schedule)) == want
