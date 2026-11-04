"""Day 73: After the Blackout."""

import copy

import pytest

from coursekit import load_module

# Three SACCO accounts. T1 moved 20 out of A and committed; T2 and T3 were still running when the power went.
LOG = [
    ("start", 1),
    ("update", 1, "A", 100, 80),
    ("start", 2),
    ("update", 2, "B", 50, 70),
    ("commit", 1),
    ("update", 2, "C", 10, 0),
    ("start", 3),
    ("update", 3, "A", 80, 90),
]
AFTER = {"A": 80, "B": 50, "C": 10}


@pytest.fixture
def r(target):
    return load_module(target / "recovery_log.py")


def test_losers(r):
    assert r.losers(LOG) == [2, 3]
    assert r.losers(LOG + [("abort", 3), ("commit", 2)]) == []
    assert r.losers([("start", 4), ("checkpoint", (4,)), ("start", 1)]) == [1, 4]


def check(recover, log, disk, want):
    before = copy.deepcopy(disk)
    got = recover(log, disk)
    assert disk == before, "don't change the dict you were given"
    assert got == want
    assert recover(log, got) == want, "recovering twice (a crash during recovery) must give the same answer"


@pytest.mark.parametrize("disk", [
    {"A": 90, "B": 70, "C": 0},
    {"A": 80, "B": 50, "C": 0},
    {"A": 90, "B": 50, "C": 10},
    {"A": 80, "B": 70, "C": 10},
])
def test_undo_recover(r, disk):
    check(r.undo_recover, LOG, disk, AFTER)


def test_undo_goes_backwards(r):
    log = [("start", 1), ("update", 1, "X", 5, 6), ("update", 1, "X", 6, 7)]
    check(r.undo_recover, log, {"X": 7}, {"X": 5})


def test_undo_leaves_finished_transactions_alone(r):
    log = [("start", 1), ("update", 1, "X", 5, 6), ("abort", 1), ("start", 2), ("update", 2, "Y", 1, 2),
           ("commit", 2)]
    check(r.undo_recover, log, {"X": 5, "Y": 2, "Z": 9}, {"X": 5, "Y": 2, "Z": 9})


@pytest.mark.parametrize("disk", [
    {"A": 100, "B": 50, "C": 10},
    {"A": 80, "B": 50, "C": 10},
])
def test_redo_recover(r, disk):
    check(r.redo_recover, LOG, disk, AFTER)


def test_redo_goes_forwards(r):
    log = [("start", 1), ("update", 1, "X", 5, 6), ("update", 1, "X", 6, 7), ("commit", 1),
           ("start", 2), ("update", 2, "X", 7, 8), ("commit", 2), ("start", 3), ("update", 3, "X", 8, 9)]
    check(r.redo_recover, log, {"X": 5}, {"X": 8})


@pytest.mark.parametrize("disk", [
    {"A": 100, "B": 50, "C": 10},
    {"A": 90, "B": 70, "C": 0},
    {"A": 100, "B": 70, "C": 10},
    {"A": 80, "B": 50, "C": 0},
])
def test_undo_redo_recover(r, disk):
    check(r.undo_redo_recover, LOG, disk, AFTER)


def test_undo_redo_with_several_winners_and_losers(r):
    log = [("start", 1), ("start", 2), ("update", 1, "P", 0, 10), ("update", 2, "Q", 0, 5), ("commit", 1),
           ("start", 3), ("update", 3, "P", 10, 15), ("update", 2, "R", 0, 1), ("start", 4),
           ("update", 4, "S", 0, 3), ("commit", 4)]
    check(r.undo_redo_recover, log, {"P": 15, "Q": 0, "R": 1, "S": 0}, {"P": 10, "Q": 0, "R": 0, "S": 3})


@pytest.mark.parametrize("log, want", [
    (LOG, 0),
    ([("start", 1), ("update", 1, "A", 1, 2), ("commit", 1), ("checkpoint", ()), ("start", 2)], 3),
    ([("start", 1), ("start", 2), ("update", 2, "B", 1, 2), ("checkpoint", (1, 2)), ("commit", 1)], 1),
    ([("start", 1), ("start", 2), ("checkpoint", (1, 2)), ("commit", 2), ("commit", 1)], 2),
    ([("start", 1), ("checkpoint", (1,)), ("start", 2), ("commit", 1), ("checkpoint", (2,)), ("start", 3)], 2),
    ([("start", 1), ("checkpoint", (1,)), ("commit", 1), ("start", 2), ("checkpoint", (2,))], 3),
])
def test_scan_from(r, log, want):
    assert r.scan_from(log) == want


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.UNDO_LOGGING_NEEDS_THE_NEW_VALUE_IN_THE_LOG, a.REDO_LOGGING_LETS_UNCOMMITTED_CHANGES_REACH_DISK,
            a.UNDO_REDO_LOGGING_LETS_DIRTY_PAGES_BE_WRITTEN_WHENEVER_THE_BUFFER_POOL_LIKES,
            a.A_CHECKPOINT_MEANS_RECOVERY_CAN_SKIP_PART_OF_THE_LOG,
            a.RECOVERY_MUST_BE_SAFE_TO_RUN_TWICE] == [False, False, True, True, True]


def test_the_setting_exists_in_mysql(target, mysql):
    a = load_module(target / "answers.py")
    assert isinstance(a.SETTING_THAT_FLUSHES_THE_LOG_AT_COMMIT, str), "a setting name, as a string"
    result = mysql.run(f"SELECT @@{a.SETTING_THAT_FLUSHES_THE_LOG_AT_COMMIT};")
    assert result.ok, f"MySQL doesn't know that setting: {result.stderr.strip()}"
    assert result.rows == [("1",)]


T1 = [("log", ("start", 1)), ("log", ("update", 1, "A", 100, 80))]


@pytest.mark.parametrize("events, want", [
    (T1 + [("flush",), ("write", "A"), ("log", ("commit", 1)), ("flush",), ("tell", 1)], None),
    (T1 + [("write", "A")], 2),
    (T1 + [("log", ("commit", 1)), ("tell", 1)], 3),
    (T1 + [("log", ("commit", 1)), ("flush",), ("tell", 1), ("write", "A")], None),
    (T1 + [("write", "B"), ("flush",), ("write", "A")], None),
    (T1 + [("flush",), ("log", ("update", 1, "A", 80, 60)), ("write", "A")], 4),
    (T1 + [("flush",), ("log", ("commit", 1)), ("tell", 1)], 4),
    ([("tell", 7)], 0),
])
def test_kata_follows_wal(r, events, want):
    assert r.follows_wal(events) == want
