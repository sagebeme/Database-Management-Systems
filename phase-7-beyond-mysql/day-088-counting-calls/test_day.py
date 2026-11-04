"""Day 88: Counting Calls."""

import pytest

from coursekit import load_module


@pytest.fixture
def ex(target):
    return load_module(target / "exercise.py")


@pytest.fixture
def cache(ex, redis_db):
    return ex.Cache(redis_db)


def test_count_calls(cache, redis_db):
    assert redis_db.get("Cache.store") is None
    cache.store(b"first")
    assert redis_db.get("Cache.store") == b"1"
    cache.store(b"second")
    cache.store(b"third")
    assert redis_db.get("Cache.store") == b"3"
    assert cache.get(cache.store("x")) == b"x", "the method still works"
    assert type(cache).store.__qualname__ == "Cache.store", "use functools.wraps, so the wrapper keeps the name"


def test_call_history(cache, redis_db):
    keys = [cache.store(v) for v in ("first", "second", "third")]
    assert redis_db.lrange("Cache.store:inputs", 0, -1) == [b"('first',)", b"('second',)", b"('third',)"]
    assert redis_db.lrange("Cache.store:outputs", 0, -1) == [k.encode() for k in keys]


def test_decorators_work_on_any_class(ex, redis_db):
    class Shop:
        def __init__(self, r):
            self._redis = r

        @ex.count_calls
        @ex.call_history
        def price(self, item, qty=1):
            return {"unga": 210, "sukari": 180}[item] * qty

    shop = Shop(redis_db)
    assert shop.price("unga", qty=2) == 420
    assert shop.price("sukari") == 180
    name = "test_decorators_work_on_any_class.<locals>.Shop.price"
    assert redis_db.get(name) == b"2"
    assert redis_db.lrange(f"{name}:inputs", 0, -1) == [b"('unga',)", b"('sukari',)"]
    assert redis_db.lrange(f"{name}:outputs", 0, -1) == [b"420", b"180"]


def test_replay(ex, cache, capsys):
    keys = [cache.store(v) for v in ("foo", "bar", 42)]
    capsys.readouterr()
    ex.replay(cache.store)
    assert capsys.readouterr().out == (
        "Cache.store was called 3 times:\n"
        f"Cache.store(*('foo',)) -> {keys[0]}\n"
        f"Cache.store(*('bar',)) -> {keys[1]}\n"
        f"Cache.store(*(42,)) -> {keys[2]}\n")


def test_replay_never_called(ex, cache, capsys):
    ex.replay(cache.store)
    assert capsys.readouterr().out == "Cache.store was called 0 times:\n"


def test_kata_record_errors(ex, cache, redis_db, capsys):
    key = cache.store(1000)
    assert cache.withdraw(key, 300) == 700
    with pytest.raises(ValueError, match="not enough"):
        cache.withdraw(key, 5000)
    with pytest.raises(ValueError, match="positive"):
        cache.withdraw(key, 0)
    assert cache.withdraw(key, 700) == 0
    assert redis_db.get("Cache.withdraw") == b"4"
    assert redis_db.get("Cache.withdraw:errors") == b"2"
    assert redis_db.lrange("Cache.withdraw:outputs", 0, -1) == [b"700", b"error: ValueError", b"error: ValueError",
                                                                 b"0"], "inputs and outputs stay in step"
    capsys.readouterr()
    ex.replay(cache.withdraw)
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "Cache.withdraw was called 4 times:"
    assert lines[2] == f"Cache.withdraw(*('{key}', 5000)) -> error: ValueError"
