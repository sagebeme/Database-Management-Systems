"""Day 72: Who Came First."""

import pytest

from coursekit import load_module
from coursekit.schedules import parse


@pytest.fixture
def t(target):
    return load_module(target / "timestamps.py")


def test_default_timestamps(t):
    assert t.default_timestamps(parse("r2(A) w1(A) r3(B) c2 w1(B)")) == {2: 1, 1: 2, 3: 3}
    assert t.default_timestamps(parse("")) == {}


@pytest.mark.parametrize("schedule, ts, want", [
    ("r1(A) w1(A) r2(A) w2(A) c1 c2", None, ["ok"] * 6),
    ("r2(A) w1(A) c1", None, ["ok", "ok", "ok"]),
    ("r1(A) w2(A) c2 w1(A) c1", None, ["ok", "ok", "ok", "abort", "skip"]),
    ("r1(A) r2(A) w2(A) w1(A)", None, ["ok", "ok", "ok", "abort"]),
    ("w2(A) r1(A) w1(B) c1", {1: 1, 2: 2}, ["ok", "abort", "skip", "skip"]),
    ("r1(A) w2(A) r1(A)", None, ["ok", "ok", "abort"]),
    ("r2(B) r1(A) w2(A) w1(B)", None, ["ok", "ok", "abort", "ok"]),
    ("w1(A) r1(A) w1(A) r2(A) w2(A)", {1: 5, 2: 9}, ["ok"] * 5),
    ("w1(A) a1 r2(A)", None, ["ok", "ok", "ok"]),
    ("r1(A) w2(A) w1(A) c1 c2", None, ["ok", "ok", "abort", "skip", "ok"]),
])
def test_basic_to(t, schedule, ts, want):
    assert t.basic_to(parse(schedule), ts) == want


def test_basic_to_keeps_timestamps_of_aborted_writes(t):
    s = parse("w2(A) r3(B) w2(B) r1(A)")
    assert t.basic_to(s, {1: 1, 2: 2, 3: 3}) == ["ok", "ok", "abort", "abort"], \
        "T2 was rolled back, but the WTS it set on A stays, so the older T1 can't read A"


@pytest.mark.parametrize("schedule, ts, want", [
    ("r1(A) w2(A) c2 w1(A) c1", None, ["ok", "ok", "ok", "ignore", "ok"]),
    ("r1(A) w2(A) w1(A) c1 c2", None, ["ok", "ok", "ignore", "ok", "ok"]),
    ("r1(A) r2(A) w2(A) w1(A)", None, ["ok", "ok", "ok", "abort"]),
    ("w3(A) w1(A) w2(A) r3(A)", {1: 1, 2: 2, 3: 3}, ["ok", "ignore", "ignore", "ok"]),
    ("w2(A) w1(A) r1(A)", {1: 1, 2: 2}, ["ok", "ignore", "abort"]),
])
def test_thomas_write_rule(t, schedule, ts, want):
    assert t.thomas_write_rule(parse(schedule), ts) == want


def test_aborted(t):
    s = parse("r2(A) r1(B) w1(A) w2(B) r3(A) c3")
    assert t.aborted(["ok", "ok", "abort", "abort", "ok", "ok"], s) == [1, 2]
    assert t.aborted(t.basic_to(parse("r1(A) w2(A) c2 w1(A) c1")), parse("r1(A) w2(A) c2 w1(A) c1")) == [1]


@pytest.mark.parametrize("requester, holder, ts, wd, ww", [
    (1, 2, {1: 10, 2: 20}, "wait", "wound"),
    (2, 1, {1: 10, 2: 20}, "die", "wait"),
    ("mpesa", "airtel", {"mpesa": 3, "airtel": 1}, "die", "wait"),
    ("mpesa", "airtel", {"mpesa": 1, "airtel": 3}, "wait", "wound"),
])
def test_wait_die_and_wound_wait(t, requester, holder, ts, wd, ww):
    assert t.wait_die(requester, holder, ts) == wd
    assert t.wound_wait(requester, holder, ts) == ww


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.BASIC_TIMESTAMP_ORDERING_CAN_DEADLOCK, a.BASIC_TIMESTAMP_ORDERING_SCHEDULES_ARE_CONFLICT_SERIALIZABLE,
            a.BASIC_TIMESTAMP_ORDERING_SCHEDULES_ARE_ALWAYS_RECOVERABLE,
            a.THOMAS_WRITE_RULE_SCHEDULES_ARE_ALWAYS_CONFLICT_SERIALIZABLE,
            a.IN_WAIT_DIE_A_RESTARTED_TRANSACTION_KEEPS_ITS_OLD_TIMESTAMP,
            a.IN_WOUND_WAIT_AN_OLDER_TRANSACTION_CAN_WAIT_FOR_A_YOUNGER_ONE] == [False, True, False, False, True, False]


@pytest.mark.parametrize("schedule, want", [
    ("r2(A) w1(A) c1 c2", ((2, 1), 0)),
    ("r1(A) w2(A) c2 w1(A) c1", ((1, 2), 1)),
    ("r1(A) r2(A) w2(A) w1(A)", ((1, 2), 1)),
    ("r2(B) r1(A) w2(A) w1(B)", ((1, 2), 1)),
    ("r3(A) w1(A) r1(B) w2(B) r2(C) w3(C)", ((1, 2, 3), 1)),
    ("r1(A) r2(B) r3(C)", ((1, 2, 3), 0)),
])
def test_kata_fewest_aborts(t, schedule, want):
    assert t.fewest_aborts(parse(schedule)) == want
