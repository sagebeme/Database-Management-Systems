"""Day 68: Can We Undo It?"""

import pytest

from coursekit import load_module
from coursekit.schedules import parse

# schedule, reads_from, recoverable, cascadeless, strict
CASES = [
    ("w1(A) r2(A) c2 c1", [(2, 1, "A")], False, False, False),
    ("w1(A) r2(A) c1 c2", [(2, 1, "A")], True, False, False),
    ("w1(A) c1 r2(A) c2", [(2, 1, "A")], True, True, True),
    ("w1(A) w2(A) c1 c2", [], True, True, False),
    ("r1(A) w1(A) r2(A) w2(A) r3(A) c3 a1", [(2, 1, "A"), (3, 2, "A")], False, False, False),
    ("w1(A) a1 r2(A) c2", [], True, True, True),
    ("w1(A) w2(A) a2 r3(A) c1 c3", [(3, 1, "A")], True, False, False),
    ("w1(A) r2(A) a1 c2", [(2, 1, "A")], False, False, False),
    ("r1(A) r2(A) c1 c2", [], True, True, True),
    ("w1(A) r2(A) w2(B) r3(B) c1 c2 c3", [(2, 1, "A"), (3, 2, "B")], True, False, False),
    ("w1(A) r1(A) w2(B) c2 r1(B) c1", [(1, 2, "B")], True, True, True),
    ("w1(A) r2(A)", [(2, 1, "A")], True, False, False),
    ("w2(A) w1(B) r1(A) r2(B) c2 c1", [(1, 2, "A"), (2, 1, "B")], False, False, False),
]


@pytest.fixture
def r(target):
    return load_module(target / "recovery.py")


@pytest.mark.parametrize("schedule, want", [case[:2] for case in CASES])
def test_reads_from(r, schedule, want):
    assert r.reads_from(parse(schedule)) == want


@pytest.mark.parametrize("schedule, recoverable, cascadeless, strict", [(c[0], *c[2:]) for c in CASES])
def test_properties(r, schedule, recoverable, cascadeless, strict):
    s = parse(schedule)
    assert (r.is_recoverable(s), r.is_cascadeless(s), r.is_strict(s)) == (recoverable, cascadeless, strict)


@pytest.mark.parametrize("schedule, aborting, want", [
    ("r1(A) w1(A) r2(A) w2(A) r3(A)", 1, [2, 3]),
    ("r1(A) w1(A) r2(A) w2(A) r3(A)", 2, [3]),
    ("w1(A) r2(A) r3(A) w4(B) r5(B)", 1, [2, 3]),
    ("w1(A) w2(B) r3(B) w3(C) r4(C)", 1, []),
    ("w1(A) w2(B) r3(B) w3(C) r4(C)", 2, [3, 4]),
])
def test_cascade(r, schedule, aborting, want):
    assert r.cascade(parse(schedule), aborting) == want


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.EVERY_STRICT_SCHEDULE_IS_CASCADELESS, a.EVERY_CASCADELESS_SCHEDULE_IS_RECOVERABLE,
            a.EVERY_RECOVERABLE_SCHEDULE_IS_CASCADELESS, a.EVERY_SERIAL_SCHEDULE_IS_STRICT,
            a.A_SCHEDULE_WITH_NO_READS_FROM_OTHERS_IS_ALWAYS_STRICT] == [True, True, False, True, False]


@pytest.mark.parametrize("schedule, want", [
    ("w1(A) r2(A) c2 c1", "not recoverable"),
    ("w1(A) r2(A) c1 c2", "recoverable"),
    ("w1(A) w2(A) c1 c2", "cascadeless"),
    ("w1(A) c1 r2(A) c2", "strict"),
    ("r1(A) w1(A) c1 r2(A) w2(A) c2", "strict"),
])
def test_kata_classify(r, schedule, want):
    assert r.classify(parse(schedule)) == want
