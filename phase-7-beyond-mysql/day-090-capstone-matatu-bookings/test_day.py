"""Day 90 capstone: Matatu Bookings."""

import threading
from datetime import datetime, timezone

import pymongo
import pytest

from coursekit import load_module

SEED = """
INSERT INTO routes (number, fare) VALUES ('46', 70), ('111', 100), ('125', 120);
INSERT INTO trips (route, departs, seats) VALUES
    ('46', '2026-03-02 07:00+03', 14),
    ('111', '2026-03-02 07:30+03', 33),
    ('125', '2026-03-02 08:00+03', 4);
"""
A, B, C = "254711000001", "254722000002", "254733000003"


@pytest.fixture
def b(target):
    return load_module(target / "bookings.py")


@pytest.fixture
def pg(postgres, target):
    postgres.run_file(target / "schema.sql").check()
    postgres.run(SEED).check()
    return postgres


@pytest.fixture
def mongo_db(mongo, mongo_url):
    client = pymongo.MongoClient(mongo_url)
    yield client[mongo.database]
    client.close()


@pytest.fixture
def svc(b, pg, redis_db, mongo_db):
    conn = pg.connect()
    yield b.Bookings(conn, redis_db, mongo_db)
    conn.close()


def events(mongo_db, kind=None):
    query = {} if kind is None else {"type": kind}
    return [{k: v for k, v in e.items() if k not in ("_id", "at")} for e in mongo_db.events.find(query).sort("_id", 1)]


# The schema

def test_schema(pg):
    assert not pg.run("INSERT INTO routes VALUES ('58', 0);").ok, "fares are above 0"
    assert not pg.run("INSERT INTO trips (route, departs, seats) VALUES ('999', now(), 14);").ok, "a real route"
    assert not pg.run("INSERT INTO trips (route, departs, seats) VALUES ('46', now(), 71);").ok
    assert not pg.run("INSERT INTO trips (id, route, departs, seats) VALUES (50, '46', now(), 14);").ok, "identity"
    pg.run("INSERT INTO bookings (trip_id, seat, phone) VALUES (1, 3, '254711000001');").check()
    assert not pg.run("INSERT INTO bookings (trip_id, seat, phone) VALUES (1, 3, '254722000002');").ok, \
        "one booking per seat per trip"
    pg.run("INSERT INTO bookings (trip_id, seat, phone) VALUES (2, 3, '254722000002');").check()
    assert not pg.run("INSERT INTO bookings (trip_id, seat, phone) VALUES (9, 1, '254722000002');").ok
    assert not pg.run("INSERT INTO bookings (trip_id, seat, phone) VALUES (1, 0, '254722000002');").ok
    assert pg.run("SELECT booked_at IS NOT NULL FROM bookings LIMIT 1;").check().rows == [("t",)]


# Routes and the cache

def test_routes_are_cached(svc, pg, redis_db):
    assert svc.routes() == [("111", 100), ("125", 120), ("46", 70)]
    assert 55 <= redis_db.ttl("cache:routes") <= 60
    pg.run("UPDATE routes SET fare = 999;").check()
    assert svc.routes() == [("111", 100), ("125", 120), ("46", 70)], "the second read comes from Redis"


def test_set_fare_clears_the_cache(svc, mongo_db):
    svc.routes()
    svc.set_fare("46", 80)
    assert ("46", 80) in svc.routes()
    assert events(mongo_db) == [{"type": "fare_changed", "route": "46", "fare": 80}]
    with pytest.raises(Exception, match="58"):
        svc.set_fare("58", 60)


# Holding and booking

def test_hold_and_confirm(svc, pg, redis_db, mongo_db):
    svc.hold_seat(1, 5, A)
    assert redis_db.get("hold:1:5") == A.encode()
    assert 115 <= redis_db.ttl("hold:1:5") <= 120
    booking = svc.confirm(1, 5, A)
    assert isinstance(booking, int)
    assert pg.run("SELECT trip_id, seat, phone FROM bookings;").check().rows == [("1", "5", A)]
    assert redis_db.get("hold:1:5") is None
    assert events(mongo_db) == [{"type": "held", "trip": 1, "seat": 5, "phone": A},
                                {"type": "booked", "trip": 1, "seat": 5, "phone": A}]
    assert isinstance(mongo_db.events.find_one()["at"], datetime)


@pytest.mark.parametrize("trip, seat", [(1, 0), (1, 15), (3, 5), (99, 1)])
def test_hold_refuses_seats_that_dont_exist(b, svc, trip, seat):
    with pytest.raises(b.BookingError):
        svc.hold_seat(trip, seat, A)


def test_hold_refuses_taken_seats(b, svc, mongo_db):
    svc.hold_seat(1, 5, A)
    with pytest.raises(b.BookingError):
        svc.hold_seat(1, 5, B)
    svc.hold_seat(1, 5, A)
    svc.confirm(1, 5, A)
    with pytest.raises(b.BookingError):
        svc.hold_seat(1, 5, B)
    with pytest.raises(b.BookingError):
        svc.hold_seat(1, 5, A)
    assert len(events(mongo_db, "held")) == 2


def test_holding_again_restarts_the_clock(svc, redis_db):
    svc.hold_seat(1, 5, A)
    redis_db.expire("hold:1:5", 10)
    svc.hold_seat(1, 5, A)
    assert redis_db.ttl("hold:1:5") > 100


def test_confirm_needs_your_own_hold(b, svc, pg, redis_db):
    with pytest.raises(b.BookingError):
        svc.confirm(1, 5, A)
    svc.hold_seat(1, 5, A)
    with pytest.raises(b.BookingError):
        svc.confirm(1, 5, B)
    redis_db.delete("hold:1:5")
    with pytest.raises(b.BookingError):
        svc.confirm(1, 5, A)
    assert pg.run("SELECT count(*) FROM bookings;").check().rows == [("0",)]


def test_release(svc, redis_db, mongo_db):
    svc.hold_seat(2, 9, A)
    assert svc.release(2, 9, B) is False
    assert redis_db.get("hold:2:9") == A.encode()
    assert svc.release(2, 9, A) is True
    assert redis_db.get("hold:2:9") is None
    assert svc.release(2, 9, A) is False
    assert events(mongo_db, "released") == [{"type": "released", "trip": 2, "seat": 9, "phone": A}]


def test_free_seats(svc, redis_db):
    assert svc.free_seats(3) == [1, 2, 3, 4]
    svc.hold_seat(3, 2, A)
    svc.hold_seat(3, 4, B)
    svc.confirm(3, 4, B)
    svc.hold_seat(1, 1, C)
    assert svc.free_seats(3) == [1, 3]
    redis_db.delete("hold:3:2")
    assert svc.free_seats(3) == [1, 2, 3], "an expired hold frees the seat"


def test_eight_passengers_one_seat(svc, b, pg, redis_db, mongo_db):
    gate = threading.Barrier(8)
    won = []

    def tap(n):
        conn = pg.connect()
        service = b.Bookings(conn, redis_db, mongo_db)
        phone = f"2547000000{n:02d}"
        gate.wait()
        try:
            service.hold_seat(2, 1, phone)
            won.append(phone)
        except b.BookingError:
            pass
        finally:
            conn.close()

    threads = [threading.Thread(target=tap, args=(n,)) for n in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(won) == 1, "the hold must be one atomic SET NX, not a GET then a SET"


# The kata

def test_kata_trip_report(svc, mongo_db):
    assert svc.trip_report(2) == {"booked": 0, "takings": 0, "holds_given_up": 0, "busiest_hour": None}
    for seat, phone in ((1, A), (2, B), (3, C)):
        svc.hold_seat(2, seat, phone)
    svc.confirm(2, 1, A)
    svc.confirm(2, 2, B)
    svc.release(2, 3, C)
    svc.hold_seat(1, 1, A)
    svc.release(1, 1, A)
    # The three holds above happened this hour; hour 4 gets four, so it wins whatever the time is now.
    mongo_db.events.insert_many([
        {"type": "held", "trip": 2, "seat": 9, "phone": C, "at": datetime(2026, 3, 2, 4, 10, tzinfo=timezone.utc)},
        {"type": "held", "trip": 2, "seat": 8, "phone": C, "at": datetime(2026, 3, 2, 4, 50, tzinfo=timezone.utc)},
        {"type": "held", "trip": 2, "seat": 7, "phone": C, "at": datetime(2026, 3, 2, 4, 55, tzinfo=timezone.utc)},
        {"type": "held", "trip": 2, "seat": 5, "phone": C, "at": datetime(2026, 3, 2, 4, 58, tzinfo=timezone.utc)},
        {"type": "held", "trip": 2, "seat": 6, "phone": C, "at": datetime(2026, 3, 2, 5, 0, tzinfo=timezone.utc)},
        {"type": "booked", "trip": 2, "seat": 6, "phone": C, "at": datetime(2026, 3, 2, 4, 0, tzinfo=timezone.utc)},
    ])
    assert svc.trip_report(2) == {"booked": 2, "takings": 200, "holds_given_up": 1, "busiest_hour": 4}
    with pytest.raises(Exception):
        svc.trip_report(99)
