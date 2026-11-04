"""Day 88: counting calls, with decorators that write to Redis.

The decorators go on methods of a class whose instances keep a redis.Redis client in self._redis. Each one uses
the method's __qualname__ ("Cache.store") as the start of its keys.
"""

import uuid
from functools import wraps


def count_calls(method):
    """Count every call of the method at the key <qualname> ("Cache.store"), with INCR, then call it."""
    return method  # replace this line: for now the method is left as it was


def call_history(method):
    """Push str(args) to the list <qualname>:inputs before the call, and str(the result) to <qualname>:outputs
    after it, with RPUSH. Return the result."""
    return method  # replace this line: for now the method is left as it was


def record_errors(method):
    """Kata: if the method raises, INCR <qualname>:errors, RPUSH "error: <the exception's class name>" to
    <qualname>:outputs, and raise the exception again. Otherwise just return the result."""
    return method  # replace this line: for now the method is left as it was


class Cache:
    """Day 87's Cache, with its methods decorated. (Done for you.)"""

    def __init__(self, client):
        self._redis = client

    @count_calls
    @call_history
    def store(self, data):
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key, fn=None):
        value = self._redis.get(key)
        return value if value is None or fn is None else fn(value)

    @count_calls
    @call_history
    @record_errors
    def withdraw(self, key, amount):
        """Take amount off the number stored at key and return what's left. ValueError if amount isn't positive
        or there isn't enough."""
        if amount <= 0:
            raise ValueError("amount must be positive")
        balance = int(self._redis.get(key) or 0)
        if amount > balance:
            raise ValueError("not enough")
        return self._redis.decrby(key, amount)


def replay(method):
    """Print the history of calls of a decorated method, given as a bound method (cache.store), exactly so:

    Cache.store was called 3 times:
    Cache.store(*('foo',)) -> 13bf32a9-a249-4664-95fd-ab2b0c8e6e2a
    Cache.store(*('bar',)) -> dcddd00c-4219-4dd7-8877-66afbe8e7df8
    Cache.store(*(42,)) -> 5e752f2b-ecd8-4925-a3ce-e2efdee08d20

    The count comes from count_calls' key (0 if it isn't there); the lines pair up inputs and outputs in order."""
    raise NotImplementedError("write this")
