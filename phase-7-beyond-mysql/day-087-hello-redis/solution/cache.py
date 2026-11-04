"""Day 87: hello, Redis.

`client` is a redis.Redis connection, made by whoever calls you:
    client = redis.Redis(host="127.0.0.1", port=6380)
Redis hands values back as bytes (b"42"), or None for a key that isn't there.
"""

import uuid


class Cache:
    def __init__(self, client):
        """Keep the client as self._redis."""
        self._redis = client

    def store(self, data):
        """Store data (str, bytes, int or float) under a new random key (a uuid4, as a string) and return the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key, fn=None):
        """The value stored at key, passed through fn if fn is given (but never call fn on a missing key: return
        None)."""
        value = self._redis.get(key)
        if value is None or fn is None:
            return value
        return fn(value)

    def get_str(self, key):
        """The value as a str (UTF-8), or None."""
        return self.get(key, lambda b: b.decode("utf-8"))

    def get_int(self, key):
        """The value as an int, or None."""
        return self.get(key, int)


def send_otp(client, phone, code, seconds=300):
    """Keep a one-time PIN for phone at the key otp:<phone>, for `seconds` seconds. A new code replaces the old
    one and resets the wrong-guess count at otp_tries:<phone>."""
    client.set(f"otp:{phone}", code, ex=seconds)
    client.delete(f"otp_tries:{phone}")


def check_otp(client, phone, code, max_tries=3):
    """True if code is the phone's current PIN. A right code works once: delete it. Count wrong guesses at
    otp_tries:<phone> (expiring with the PIN); on the max_tries-th wrong guess, delete the PIN too."""
    key, tries = f"otp:{phone}", f"otp_tries:{phone}"
    current = client.get(key)
    if current is None:
        return False
    if current.decode() == str(code):
        client.delete(key, tries)
        return True
    wrong = client.incr(tries)
    client.expire(tries, max(client.ttl(key), 1))
    if wrong >= max_tries:
        client.delete(key, tries)
    return False


def rate_limited(client, phone, limit, window):
    """Kata: a fixed-window rate limit for M-Pesa payment prompts. Count this request at the key
    rate:<phone>, which expires `window` seconds after the window's first request. Return True if this
    request is over the limit (the limit+1-th or later in the window), False if it's allowed."""
    key = f"rate:{phone}"
    count = client.incr(key)
    if count == 1:
        client.expire(key, window)
    return count > limit
