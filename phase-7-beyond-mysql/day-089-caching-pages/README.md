# Day 89: Caching Pages

## The brief

The sacco's timetable page is built from a slow API, and every passenger at Kencom refreshes it at 5:30 pm. Fetching it once and keeping the copy for ten seconds turns a thousand slow requests into one: an **expiring cache**, the most common use of Redis in the world.

Redis is more than strings, though. It has lists, sets, hashes and sorted sets, each with atomic commands, and they answer questions that are awkward anywhere else: who's next in the queue for a ride, who rides every day, which seats are taken, which drivers lead the month. Today you'll use all of them.

## What you'll use

**Expiring cache** (cache-aside): look in the cache; if it's there, use it; if not, do the slow thing and store the result with an expiry.

```python
cached = r.get(f"cached:{url}")
if cached is None:
    page = fetch(url)                         # slow
    r.set(f"cached:{url}", page, ex=10)       # or r.setex(key, 10, page)
```

The catch: for up to ten seconds people see an old timetable. Every cache trades freshness for speed; the expiry is how much staleness you accept.

**The other types**:

| Type | Like | Commands |
|---|---|---|
| list | a queue or stack | `LPUSH` / `RPUSH` add at the left / right; `LPOP` / `RPOP` take from the left / right; `LRANGE`, `LLEN` |
| set | a bag of unique strings | `SADD`, `SCARD` (how many), `SISMEMBER`, `SINTER` / `SUNION` / `SDIFF` across sets |
| hash | a small dict under one key | `HSET`, `HGET`, `HGETALL`, `HSETNX` (set only if the field is empty), `HINCRBY` |
| sorted set | a set where each member has a score, kept in score order | `ZADD`, `ZINCRBY`, `ZREVRANGE ... WITHSCORES`, `ZCARD`, `ZREMRANGEBYSCORE` |

`LPUSH` then `RPOP` makes a first-in, first-out queue: new ones go in on the left, old ones come out on the right.

Every command is **atomic**. `HSETNX` checks and sets in one step, so when eight passengers tap seat 7 at the same moment, exactly one gets it, with no lock and no transaction.

In redis-py, the Python names are the commands in lower case: `r.lpush(...)`, `r.sinter([...])`, `r.hsetnx(...)`, `r.zrevrange(key, 0, n - 1, withscores=True)`. Everything comes back as bytes; scores come back as floats.

## Steps

1. `starter/web.py`: `get_page`. `fetch` is done.
2. `starter/rides.py`: the queue, the riders, the seats and the leaderboard.
3. `pytest phase-7-beyond-mysql/day-089-caching-pages`

The tests run a little web server on your machine that says how many times each page was fetched, so they can tell a cached page from a fresh one.

## The kata: A Sliding Window

Day 87's fixed window has a weakness: five requests at 0:59 and five more at 1:01 all get through, ten in two seconds, because they fall in different windows. In `starter/rides.py`, write `allowed(client, phone, limit, window, now)` with a **sorted set** of request times: drop the old ones, count the rest, and record this one only if it's allowed.

## When you're stuck

- **The second `get_page` still fetches**: look in `cached:<url>` *before* calling `fetch`, and decode what you find.
- **The count is 1 after two calls**: `INCR` the count on every call, before you check the cache.
- **The queue comes out backwards**: `LPUSH` adds on the left, so take from the right with `RPOP`.
- **`regulars` with no days raises `wrong number of arguments for 'sinter'`**: `SINTER` needs at least one key. Return `[]` first.
- **`seat_map` has `b'1'` keys**: convert each field with `int(...)` and each value with `.decode()`.
- **`top_drivers` gives `50.0`**: sorted-set scores are floats. `int(...)` them.
- **The kata lets the 4th request through**: count with `ZCARD` *after* removing old times with `ZREMRANGEBYSCORE`, and `ZADD` only if you're under the limit.
