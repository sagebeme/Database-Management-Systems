"""Day 69: As If One at a Time."""

import pytest

from coursekit import load_module
from coursekit.schedules import parse

# schedule, graph, conflict serializable, serial orders
CASES = [
    ("r1(A) w2(A) w1(A)", {1: [2], 2: [1]}, False, []),
    ("r1(A) r2(B) w1(B) w2(A) r3(A)", {1: [2], 2: [1, 3], 3: []}, False, []),
    ("r1(A) w1(A) r2(A) w2(A) r1(B) w1(B) r2(B) w2(B)", {1: [2], 2: []}, True, [(1, 2)]),
    ("r1(A) r2(A) r3(B) w1(A) w3(B) c1 c2 c3", {1: [], 2: [1], 3: []}, True, [(2, 1, 3), (2, 3, 1), (3, 2, 1)]),
    ("r2(A) r1(B) w2(A) r3(A) w1(B) w3(A) r2(B) w2(B)", {1: [2], 2: [3], 3: []}, True, [(1, 2, 3)]),
    ("r1(A) r2(A) r3(A)", {1: [], 2: [], 3: []}, True,
     [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]),
    ("w1(A) w2(B) w3(C) r1(C) r2(A) r3(B)", {1: [2], 2: [3], 3: [1]}, False, []),
]


@pytest.fixture
def s(target):
    return load_module(target / "serial.py")


def test_conflicts(s):
    assert s.conflicts(parse("r1(A) r2(B) w1(B) w2(A) r3(A)")) == [(2, 1, "B"), (1, 2, "A"), (2, 3, "A")]
    assert s.conflicts(parse("r1(A) r2(A) w1(B) w2(C) c1 c2")) == [], "reads don't conflict; neither do different items"
    assert s.conflicts(parse("w1(A) w1(A) r1(A)")) == [], "a transaction doesn't conflict with itself"
    assert s.conflicts(parse("w1(A) r2(A) w1(A) w2(A)")) == [(1, 2, "A"), (2, 1, "A")]


@pytest.mark.parametrize("schedule, graph, serializable, orders", CASES)
def test_graphs(s, schedule, graph, serializable, orders):
    ops = parse(schedule)
    assert s.precedence_graph(ops) == graph
    assert s.is_conflict_serializable(ops) is serializable
    assert s.serial_orders(ops) == orders


@pytest.mark.parametrize("graph, cycle", [
    ({1: [2], 2: [3], 3: []}, False), ({1: [2], 2: [3], 3: [1]}, True), ({1: [1]}, True),
    ({1: [], 2: [], 3: []}, False), ({1: [2, 3], 2: [4], 3: [4], 4: []}, False), ({1: [2], 2: [], 3: [4], 4: [3]}, True),
])
def test_has_cycle(s, graph, cycle):
    assert s.has_cycle(graph) is cycle


def test_conflict_equivalent(s):
    assert s.conflict_equivalent(parse("r1(A) w1(A) r2(B) w2(B)"), parse("r2(B) r1(A) w2(B) w1(A)"))
    assert not s.conflict_equivalent(parse("r1(A) w2(A)"), parse("w2(A) r1(A)")), "the conflict flipped"
    assert not s.conflict_equivalent(parse("r1(A) w2(A)"), parse("r1(A) w2(B)")), "different operations"
    assert s.conflict_equivalent(parse("r1(A) w2(A) c1 c2"), parse("r1(A) c1 w2(A) c2"))


def test_answers(target):
    a = load_module(target / "answers.py")
    assert a.S_EDGES == {(1, 2), (2, 1), (2, 3)} and a.S_IS_CONFLICT_SERIALIZABLE is False
    assert (a.INTERLEAVINGS, a.SERIALIZABLE_INTERLEAVINGS) == (6, 2)
    assert [a.TWO_READS_OF_THE_SAME_ITEM_CONFLICT, a.A_SERIAL_SCHEDULE_IS_ALWAYS_CONFLICT_SERIALIZABLE] == [False, True]


@pytest.mark.parametrize("t1, t2, want", [
    ("r1(A) w1(A)", "r2(A) w2(A)", 2),
    ("r1(A) w1(A)", "r2(B) w2(B)", 6),
    ("r1(A) r1(B)", "w2(A)", 3),
    ("r1(A) w1(B)", "r2(B) w2(A)", 2),
    ("r1(A) w1(A) r1(B) w1(B)", "r2(A) w2(A) r2(B) w2(B)", 12),
])
def test_kata_count_serializable(s, t1, t2, want):
    assert s.count_serializable(parse(t1), parse(t2)) == want
