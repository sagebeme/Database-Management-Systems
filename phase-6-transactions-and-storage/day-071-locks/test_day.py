"""Day 71: Locks."""

import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pymysql
import pytest

from coursekit import load_module
from coursekit.schedules import parse

A, B = "254711000001", "254722000002"


@pytest.fixture
def lk(target):
    return load_module(target / "locks.py")


@pytest.mark.parametrize("schedule, well_formed, two_pl, strict", [
    ("sl1(A) r1(A) sl2(A) r2(A) u1(A) u2(A)", True, True, True),
    ("xl1(A) w1(A) sl2(A) r2(A)", False, True, True),
    ("sl1(A) r1(A) xl1(A) w1(A) u1(A)", True, True, False),
    ("sl1(A) sl2(A) xl1(A)", False, True, True),
    ("r1(A)", False, True, True),
    ("sl1(A) w1(A)", False, True, True),
    ("u1(A)", False, True, True),
    ("xl1(A) w1(A) u1(A) xl1(B) w1(B) u1(B)", True, False, False),
    ("xl1(A) w1(A) xl1(B) u1(A) w1(B) u1(B) c1", True, True, False),
    ("xl1(A) w1(A) xl1(B) w1(B) c1 sl2(A) r2(A) c2", True, True, True),
    ("sl1(A) r1(A) xl2(B) w2(B) u1(A) sl1(B)", False, False, False),
])
def test_lock_rules(lk, schedule, well_formed, two_pl, strict):
    ops = parse(schedule)
    assert (lk.is_well_formed(ops), lk.follows_2pl(ops), lk.follows_strict_2pl(ops)) == (well_formed, two_pl, strict)


@pytest.mark.parametrize("holds, wants, want", [
    ({1: {"A": "X"}, 2: {"B": "X"}}, {1: ("B", "X"), 2: ("A", "S")}, [1, 2]),
    ({1: {"A": "S"}, 2: {"A": "S"}}, {1: ("A", "X"), 2: ("A", "X")}, [1, 2]),
    ({1: {"A": "S"}, 2: {"B": "X"}}, {1: ("B", "S")}, []),
    ({1: {"A": "S"}, 2: {"A": "S"}}, {1: ("A", "S")}, []),
    ({1: {"A": "X"}, 2: {"B": "X"}, 3: {"C": "X"}, 4: {}}, {1: ("B", "X"), 2: ("C", "X"), 3: ("A", "X"), 4: ("A", "S")},
     [1, 2, 3]),
])
def test_deadlocked(lk, holds, wants, want):
    assert lk.deadlocked(holds, wants) == want


@pytest.fixture
def bank(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def opposite_transfers(db, transfer):
    """A sends B 100 while B sends A 300, both at once. Returns each side's result or exception."""
    gate = threading.Barrier(2)

    def side(args):
        conn = db.connect()
        try:
            gate.wait()
            return transfer(conn, *args, pause=lambda: time.sleep(0.3))
        except pymysql.err.OperationalError as e:
            return e
        finally:
            conn.close()

    with ThreadPoolExecutor(2) as pool:
        return list(pool.map(side, [(A, B, 100), (B, A, 300)]))


def balances(db):
    return db.run("SELECT phone, balance FROM accounts ORDER BY phone;").check().rows


@pytest.mark.passes_on_starter
def test_naive_transfers_deadlock(bank, day):
    transfers = load_module(day / "starter" / "transfers.py")
    results = opposite_transfers(bank, transfers.transfer_naive)
    errors = [r for r in results if isinstance(r, Exception)]
    assert len(errors) == 1 and errors[0].args[0] == 1213, "MySQL picks one victim and rolls it back"


def test_ordered_transfers(bank, target):
    transfers = load_module(target / "transfers.py")
    results = opposite_transfers(bank, transfers.transfer_ordered)
    assert not [r for r in results if isinstance(r, Exception)], "no deadlock"
    assert balances(bank) == [(A, "10200"), (B, "9800")]


def test_transfer_with_retry(bank, target):
    transfers = load_module(target / "transfers.py")
    attempts = opposite_transfers(bank, transfers.transfer_with_retry)
    assert sorted(attempts) == [1, 2], "the victim tried again and got through"
    assert balances(bank) == [(A, "10200"), (B, "9800")]


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.TWO_PHASE_LOCKING_GUARANTEES_CONFLICT_SERIALIZABILITY, a.TWO_PHASE_LOCKING_PREVENTS_DEADLOCKS,
            a.STRICT_2PL_SCHEDULES_ARE_CASCADELESS, a.SELECT_FOR_UPDATE_TAKES_AN_EXCLUSIVE_LOCK,
            a.INNODB_PICKS_A_VICTIM_INSTEAD_OF_WAITING_FOREVER_IN_A_DEADLOCK] == [True, False, True, True, True]


@pytest.mark.parametrize("schedule, possible", [
    ("r1(A) w1(A) c1 r2(A) c2", True),
    ("r1(A) r2(A) c1 c2", True),
    ("r1(A) r2(A) w1(A) c1 c2", False),
    ("r1(A) w2(A) c1 c2", False),
    ("r1(A) c1 w2(A) c2", True),
    ("r1(A) r2(B) w1(B) c1 w2(A) c2", False),
    ("w1(A) w1(B) c1 r2(A) r2(B) c2", True),
])
def test_kata_possible_under_rigorous_2pl(lk, schedule, possible):
    assert lk.possible_under_rigorous_2pl(parse(schedule)) is possible
