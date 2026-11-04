# Day 87: Hello, Redis

## The brief

The matatu booking app sends a one-time PIN by SMS when a passenger logs in. The PIN must vanish after five minutes, work exactly once, and lock after three wrong guesses. The app also has to stop anyone triggering fifty M-Pesa payment prompts on someone else's phone. None of that belongs in Postgres: it's small, short-lived, read and written constantly, and fine to lose in a crash.

That's **Redis**: an in-memory key-value store that answers in well under a millisecond, with keys that expire on their own. Almost every busy web app has one beside its main database, for caches, sessions, PINs, rate limits, queues and counters.

## What you'll use

```bash
redis-cli -p 6380
127.0.0.1:6380> SET greeting "Habari"
127.0.0.1:6380> GET greeting
"Habari"
127.0.0.1:6380> SET otp:254711000001 4821 EX 300     # expires in 300 seconds
127.0.0.1:6380> TTL otp:254711000001                 # seconds left (-1: never expires, -2: no such key)
127.0.0.1:6380> INCR visits                          # atomic +1, starting from 0; returns the new value
127.0.0.1:6380> EXPIRE visits 60
127.0.0.1:6380> DEL greeting
127.0.0.1:6380> KEYS *                               # fine on your laptop, never on a busy server
```

From Python, with **redis-py**:

```python
import redis
r = redis.Redis(host="127.0.0.1", port=6380)
r.set("otp:254711000001", "4821", ex=300)
r.get("otp:254711000001")      # b'4821': always bytes back, or None
r.incr("visits")               # 1, 2, 3, ...
```

**Everything comes back as bytes.** Store `42` and you get `b"42"`. Turn it back yourself: `.decode("utf-8")` for text, `int(...)` for numbers.

**Key names are your schema**: `otp:254711000001`, `rate:254711000001`. A prefix and a colon keep different kinds of keys apart.

**`INCR` is atomic.** Two app servers incrementing the same key at the same moment always end up 2 apart, with no transaction or lock. That's what makes counters and rate limits easy and safe.

**A fixed-window rate limit**: `INCR` the counter; if the result is 1, it's the window's first request, so `EXPIRE` it for the window's length. Over the limit, refuse. When the key expires, a new window starts at 0.

## Steps

```bash
redis-cli -p 6380 ping        # PONG
```

Try the commands above in `redis-cli`, then:

1. `starter/cache.py`: the `Cache` class: `__init__`, `store`, `get`, `get_str`, `get_int`.
2. `send_otp` and `check_otp`.
3. `pytest phase-7-beyond-mysql/day-087-hello-redis`

The tests use a Redis database emptied before and after each test. Some wait a second or so, for keys to expire.

## The kata: Stop the Payment Spam

In `starter/cache.py`, write `rate_limited(client, phone, limit, window)`: count the request, start the window's expiry on its first request, and say whether this one is over the limit.

## When you're stuck

- **`get_str` returns `"b'foo'"`**: that's `str(b"foo")`. Decode bytes: `b"foo".decode("utf-8")`.
- **`get_int` returns a huge number**: `int.from_bytes(b"42", ...)` reads the bytes as binary. `int(b"42")` reads the digits.
- **`AttributeError: 'NoneType' object has no attribute 'decode'`**: the key isn't there. Check for `None` before calling `fn`.
- **The PIN check says the right code is wrong**: Redis gave you `b"4821"`; the caller gave you `"4821"` or `4821`. Compare `current.decode()` with `str(code)`.
- **The wrong-guess counter never expires**: `INCR` on a missing key makes a key with no expiry. Give it one (the PIN's `TTL` is a good choice).
- **The rate-limit window keeps sliding**: call `EXPIRE` only when `INCR` returns 1.
