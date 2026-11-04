# Day 88: Counting Calls

## The brief

The booking app's `Cache` is busy, and the team wants to know how busy: how many times each method is called, with what, and what it returned. They want it without touching the method bodies, because there are dozens of methods and nobody wants `self._redis.incr(...)` pasted into each one.

A **decorator** wraps a function in another function that runs code before and after it. Write the counting once, put `@count_calls` above any method, and it's counted. Today the decorators write into Redis: a counter with `INCR`, and a history of inputs and outputs in Redis **lists**. Then you'll replay the history, the way you'd investigate "what did the app do just before it went wrong?"

## What you'll use

**A decorator** takes a function and returns a new one:

```python
from functools import wraps

def shout(method):
    @wraps(method)                       # keep method's name, docstring and __qualname__
    def wrapper(self, *args, **kwargs):
        print("calling", method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    @shout
    def store(self, data): ...           # the same as: store = shout(store)
```

`method.__qualname__` is `"Cache.store"`: the class and method name, a good Redis key. Without `@wraps`, the wrapper's name would be `wrapper`, and every decorated method would share one key.

Decorators stack: the one nearest `def` wraps first, so `@count_calls` on top of `@call_history` counts the call, then records it.

**Redis lists** keep things in order:

```python
r.rpush("Cache.store:inputs", "('foo',)")    # add to the right-hand end
r.lrange("Cache.store:inputs", 0, -1)         # everything, start to end: [b"('foo',)", ...]
r.llen("Cache.store:inputs")
```

**`str(args)`**: `args` is a tuple, so `str(("foo",))` is `"('foo',)"`. Store that; Redis keeps strings, not Python tuples.

**Re-raising**: inside `except Exception as e:`, a bare `raise` sends the same exception on up after you've recorded it.

## Steps

1. `starter/exercise.py`: `count_calls`, `call_history` and `replay`. `Cache` is done and already decorated; until you write the decorators they hand the method back unchanged.
2. Try it:

   ```python
   import redis, exercise
   cache = exercise.Cache(redis.Redis(port=6380))
   cache.store("foo"); cache.store("bar"); cache.store(42)
   exercise.replay(cache.store)
   ```

3. `pytest phase-7-beyond-mysql/day-088-counting-calls`

## The kata: When It Goes Wrong

`Cache.withdraw` raises `ValueError` when there isn't enough. When it does, `call_history` records the input but never the output, and the two lists fall out of step. In `starter/exercise.py`, write `record_errors`: count the error, record `"error: ValueError"` as the output, and raise it again.

## When you're stuck

- **The count key is `wrapper`**: add `@wraps(method)`, and take the key from `method.__qualname__`, not from the wrapper.
- **`TypeError: wrapper() takes 1 positional argument but 2 were given`**: accept `(self, *args, **kwargs)` and pass them all on.
- **The method returns `None` once decorated**: the wrapper has to `return` the method's result.
- **`replay` can't find the client**: `cache.store` is a bound method; `cache.store.__self__` is the `cache`, and its `_redis` is the client.
- **`replay` prints `b'...'`**: `lrange` returns bytes. Decode each one.
- **The kata's outputs list is out of step**: `record_errors` must sit *under* `call_history` (it does, in `Cache`), and push the error output before re-raising.
