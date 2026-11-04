"""Day 66: Two Tellers, One Account.

The concurrency tests run many tellers at once, each with its own connection, and pass a pause() that sleeps
between reading and writing, so a race that would happen once in a thousand times in real life happens every time.
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pytest

from coursekit import load_module
from coursekit.schedules import parse

PHONE = "254711000001"


@pytest.fixture
def sacco(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def all_at_once(db, how_many, job):
    """Run job(conn, pause) in how_many threads that start together; return their results."""
    gate = threading.Barrier(how_many)

    def one(_):
        conn = db.connect()
        try:
            gate.wait()
            return job(conn, lambda: time.sleep(0.05))
        finally:
            conn.close()

    with ThreadPoolExecutor(how_many) as pool:
        return list(pool.map(one, range(how_many)))


def balance(db):
    return int(db.run(f"SELECT balance FROM accounts WHERE phone = '{PHONE}';").check().rows[0][0])


@pytest.mark.passes_on_starter
def test_the_unsafe_teller_loses_money(sacco, day):
    tellers = load_module(day / "starter" / "tellers.py")
    results = all_at_once(sacco, 10, lambda conn, pause: tellers.withdraw_unsafe(conn, PHONE, 100, pause))
    assert all(results), "every teller thinks it worked"
    assert balance(sacco) > 500, "10 x 100 came out of 1,500, but the balance says less went"


@pytest.mark.parametrize("way", ["withdraw_atomic", "withdraw_locked"])
def test_safe_tellers(sacco, target, way):
    withdraw = getattr(load_module(target / "tellers.py"), way)
    results = all_at_once(sacco, 20, lambda conn, pause: withdraw(conn, PHONE, 100, pause))
    assert results.count(True) == 15 and results.count(False) == 5, "1,500 pays out 15 withdrawals of 100"
    assert balance(sacco) == 0


def test_safe_tellers_one_at_a_time(sacco, target):
    tellers = load_module(target / "tellers.py")
    conn = sacco.connect()
    try:
        assert tellers.withdraw_atomic(conn, PHONE, 1000) is True
        assert tellers.withdraw_atomic(conn, PHONE, 600) is False
        assert tellers.withdraw_locked(conn, PHONE, 500) is True
        assert tellers.withdraw_locked(conn, PHONE, 1) is False
    finally:
        conn.close()
    assert balance(sacco) == 0


@pytest.mark.parametrize("schedule, want", [
    ("w1(A) r2(A) c1 c2", [(2, 1, "A")]),
    ("w1(A) c1 r2(A) c2", []),
    ("w1(A) r1(A) c1", []),
    ("w1(A) w2(B) r3(B) r3(A) a2 c1 c3", [(3, 2, "B"), (3, 1, "A")]),
    ("w1(A) w2(A) c2 r3(A)", []),
    ("w1(A) w2(A) r1(A) r3(A) c1 c2", [(1, 2, "A"), (3, 2, "A")]),
])
def test_dirty_reads(target, schedule, want):
    assert load_module(target / "anomalies.py").dirty_reads(parse(schedule)) == want


@pytest.mark.parametrize("schedule, want", [
    ("r1(A) w2(A) c2 r1(A) c1", [(1, 2, "A")]),
    ("r1(A) r1(A) w2(A) c1 c2", []),
    ("r1(A) w2(B) r1(A)", []),
    ("r1(A) w1(A) r1(A)", []),
    ("r1(A) r2(A) w1(A) r2(A) w2(A) w3(A) r2(A)", [(2, 1, "A"), (2, 3, "A")]),
])
def test_non_repeatable_reads(target, schedule, want):
    assert load_module(target / "anomalies.py").non_repeatable_reads(parse(schedule)) == want


@pytest.mark.parametrize("schedule, want", [
    ("r1(A) r2(A) w2(A) w1(A) c1 c2", [(1, 2, "A")]),
    ("r1(A) r2(A) w1(A) w2(A)", [(2, 1, "A")]),
    ("r1(A) w2(A) r1(A) w1(A)", []),
    ("r1(A) w1(A) r2(A) w2(A)", []),
    ("r1(A) r1(B) w2(A) w2(B) w1(B) w1(A)", [(1, 2, "B"), (1, 2, "A")]),
])
def test_lost_updates(target, schedule, want):
    assert load_module(target / "anomalies.py").lost_updates(parse(schedule)) == want


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.A_DIRTY_READ_NEEDS_THE_WRITER_TO_BE_UNCOMMITTED,
            a.A_PHANTOM_IS_A_ROW_THAT_APPEARS_OR_DISAPPEARS_BETWEEN_TWO_READS_OF_THE_SAME_SEARCH,
            a.LOCKING_ONLY_THE_ROWS_YOU_READ_STOPS_PHANTOMS, a.ONE_UPDATE_WITH_A_WHERE_CHECK_CANNOT_LOSE_AN_UPDATE,
            a.ANOMALIES_CAN_HAPPEN_WHEN_TRANSACTIONS_RUN_ONE_AT_A_TIME] == [True, True, False, True, False]


def test_kata_double_booking(sacco, target):
    booking = load_module(target / "booking.py")
    results = all_at_once(sacco, 6, lambda conn, pause: booking.book_seat(conn, 2, "Rider", pause))
    assert results.count(True) == 2, "two seats were left on the Machakos trip"
    assert sacco.run("SELECT COUNT(*) FROM bookings WHERE trip_id = 2;").check().rows == [("4",)]
    conn = sacco.connect()
    try:
        assert booking.book_seat(conn, 1, "Kamau") is True
    finally:
        conn.close()
