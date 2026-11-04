"""Day 89: Redis's other data types, for the matatu app.

`client` is a redis.Redis connection. Return text as str and numbers as int, never bytes.
"""


# Lists: a queue of ride requests, first come, first served.

def request_ride(client, phone):
    """Add phone to the back of the queue at queue:rides."""
    raise NotImplementedError("write this")


def next_ride(client):
    """Take the phone at the front of the queue (the oldest request), or None if the queue is empty."""
    raise NotImplementedError("write this")


# Sets: who rode on which day.

def rode(client, day, phone):
    """Record that phone rode on day ("2026-03-02") in the set riders:<day>. Twice on one day counts once."""
    raise NotImplementedError("write this")


def riders(client, day):
    """How many different phones rode on day."""
    raise NotImplementedError("write this")


def regulars(client, days):
    """The phones that rode on every one of `days`, sorted. [] for no days."""
    raise NotImplementedError("write this")


# Hashes: a trip's seats.

def book_seat(client, trip, seat, phone):
    """Give seat (an int) on trip to phone in the hash seats:<trip>, only if nobody has it. True if booked."""
    raise NotImplementedError("write this")


def seat_map(client, trip):
    """{seat: phone} for every booked seat on trip, seats as ints."""
    raise NotImplementedError("write this")


# Sorted sets: the drivers' leaderboard.

def add_points(client, driver, points):
    """Add points to driver's score in the sorted set leaderboard. Return the new score as an int."""
    raise NotImplementedError("write this")


def top_drivers(client, n):
    """The n highest scores: [(driver, score)], highest first, scores as ints."""
    raise NotImplementedError("write this")


def allowed(client, phone, limit, window, now):
    """Kata: a sliding-window rate limit. Keep the times (`now`, in seconds) of phone's recent requests in the
    sorted set requests:<phone>, each time as both member and score. Drop the ones `window` seconds or more
    older than now; if fewer than `limit` remain, record this one and return True; otherwise return False and
    record nothing. Let the key expire `window` seconds after the last request it records."""
    raise NotImplementedError("write this")
