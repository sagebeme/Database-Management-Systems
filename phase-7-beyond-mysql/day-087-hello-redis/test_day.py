"""Day 87: Hello, Redis."""

import time
import uuid

import pytest

from coursekit import load_module


@pytest.fixture
def c(target):
    return load_module(target / "cache.py")


def test_store_and_get(c, redis_db):
    cache = c.Cache(redis_db)
    assert cache._redis is redis_db
    key = cache.store("Habari")
    assert isinstance(key, str) and uuid.UUID(key)
    assert redis_db.get(key) == b"Habari"
    assert cache.get(key) == b"Habari"
    assert cache.store(b"bytes") != cache.store(b"bytes"), "a new key every time"
    assert redis_db.dbsize() == 3


@pytest.mark.parametrize("value, fn, want", [
    (b"foo", None, b"foo"),
    (123, int, 123),
    ("bar", lambda d: d.decode("utf-8"), "bar"),
    (2.5, float, 2.5),
])
def test_get_with_fn(c, redis_db, value, fn, want):
    cache = c.Cache(redis_db)
    assert cache.get(cache.store(value), fn=fn) == want


def test_typed_getters(c, redis_db):
    cache = c.Cache(redis_db)
    assert cache.get_str(cache.store("Ng'ang'a Mũkami")) == "Ng'ang'a Mũkami"
    assert cache.get_int(cache.store(4200)) == 4200
    assert cache.get_int(cache.store(-7)) == -7
    called = []
    assert cache.get("not-there", lambda v: called.append(v)) is None
    assert called == [], "never call fn on a missing key"
    assert cache.get_str("not-there") is None and cache.get_int("not-there") is None


def test_send_otp(c, redis_db):
    c.send_otp(redis_db, "254711000001", "4821", seconds=120)
    assert redis_db.get("otp:254711000001") == b"4821"
    assert 115 <= redis_db.ttl("otp:254711000001") <= 120
    c.send_otp(redis_db, "254711000001", 9034)
    assert redis_db.get("otp:254711000001") == b"9034"
    assert 295 <= redis_db.ttl("otp:254711000001") <= 300


def test_check_otp_works_once(c, redis_db):
    c.send_otp(redis_db, "254711000001", "4821")
    assert c.check_otp(redis_db, "254711000001", "4821") is True
    assert c.check_otp(redis_db, "254711000001", "4821") is False, "a one-time PIN"
    assert c.check_otp(redis_db, "254799999999", "4821") is False
    c.send_otp(redis_db, "254711000002", 1234)
    assert c.check_otp(redis_db, "254711000002", 1234) is True


def test_check_otp_three_strikes(c, redis_db):
    c.send_otp(redis_db, "254711000001", "4821")
    assert c.check_otp(redis_db, "254711000001", "0000") is False
    assert c.check_otp(redis_db, "254711000001", "1111") is False
    assert redis_db.get("otp_tries:254711000001") == b"2"
    assert redis_db.ttl("otp_tries:254711000001") > 0, "the count expires too"
    assert c.check_otp(redis_db, "254711000001", "4821") is True, "two wrong guesses still leave the PIN"
    c.send_otp(redis_db, "254711000001", "5555")
    for guess in ("1", "2", "3"):
        assert c.check_otp(redis_db, "254711000001", guess) is False
    assert c.check_otp(redis_db, "254711000001", "5555") is False, "after the third wrong guess the PIN is gone"


def test_otp_expires(c, redis_db):
    c.send_otp(redis_db, "254711000001", "4821", seconds=1)
    time.sleep(1.2)
    assert c.check_otp(redis_db, "254711000001", "4821") is False


def test_kata_rate_limited(c, redis_db):
    got = [c.rate_limited(redis_db, "254711000001", 3, 60) for _ in range(5)]
    assert got == [False, False, False, True, True]
    assert c.rate_limited(redis_db, "254722000002", 3, 60) is False, "each phone has its own count"
    assert 55 <= redis_db.ttl("rate:254711000001") <= 60
    time.sleep(1)
    c.rate_limited(redis_db, "254711000001", 3, 60)
    assert redis_db.ttl("rate:254711000001") <= 59, "only the window's first request sets the expiry"


def test_kata_window_ends(c, redis_db):
    assert [c.rate_limited(redis_db, "254711000001", 1, 1) for _ in range(2)] == [False, True]
    time.sleep(1.2)
    assert c.rate_limited(redis_db, "254711000001", 1, 1) is False, "a new window"
