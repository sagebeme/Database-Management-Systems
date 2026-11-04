"""Day 90 capstone: matatu bookings across three databases.

    PostgreSQL  the truth: routes, trips and confirmed bookings (schema.sql)
    Redis       the fast and short-lived: seat holds that expire, and a cache of the route list
    MongoDB     the record of what happened: one event document per action, in the collection events

A passenger picks a seat (hold_seat), has a couple of minutes to pay, then the booking is confirmed (confirm) or
the hold runs out. Seats are numbered 1 to the trip's seats.

Redis keys:   hold:<trip_id>:<seat>  the phone holding it, expiring after HOLD_SECONDS
              cache:routes           the route list as JSON, expiring after CACHE_SECONDS
Event documents: {"type": "held" | "booked" | "released" | "fare_changed", "trip": ..., "seat": ..., "phone": ...,
                  "at": a datetime}   (fare_changed has "route" and "fare" instead of trip, seat and phone)
"""

import json
from datetime import datetime, timezone

HOLD_SECONDS = 120
CACHE_SECONDS = 60


class BookingError(Exception):
    """A booking step that can't be done: the message says why. (Done for you.)"""


class Bookings:
    def __init__(self, pg, redis_client, mongo_db):
        """pg: a psycopg connection (autocommit=True); redis_client: a redis.Redis; mongo_db: a pymongo Database.
        (Done for you.)"""
        self.pg, self.r, self.events = pg, redis_client, mongo_db.events

    def _log(self, kind, **fields):
        """Record one event in MongoDB. (Done for you.)"""
        self.events.insert_one({"type": kind, **fields, "at": datetime.now(timezone.utc)})

    def routes(self):
        """[(number, fare)] for every route, by number. Read them from the cache:routes key if it's there;
        otherwise from Postgres, and cache them as JSON for CACHE_SECONDS."""
        raise NotImplementedError("write this")

    def set_fare(self, number, fare):
        """Change a route's fare in Postgres, drop the cached route list so nobody sees the old fare, and log a
        fare_changed event. BookingError if there's no such route."""
        raise NotImplementedError("write this")

    def _seats(self, trip_id):
        """How many seats the trip has; BookingError if there's no such trip. (Done for you.)"""
        with self.pg.cursor() as cur:
            cur.execute("SELECT seats FROM trips WHERE id = %s", (trip_id,))
            row = cur.fetchone()
        if row is None:
            raise BookingError(f"no trip {trip_id}")
        return row[0]

    def _booked(self, trip_id):
        """The set of seats booked on the trip. (Done for you.)"""
        with self.pg.cursor() as cur:
            cur.execute("SELECT seat FROM bookings WHERE trip_id = %s", (trip_id,))
            return {row[0] for row in cur.fetchall()}

    def hold_seat(self, trip_id, seat, phone):
        """Hold a seat for phone for HOLD_SECONDS, with one atomic Redis SET (NX, EX). BookingError if the trip
        doesn't exist, the seat isn't on it, it's already booked, or someone else holds it. Holding a seat you
        already hold starts its clock again. Log a held event."""
        raise NotImplementedError("write this")

    def confirm(self, trip_id, seat, phone):
        """Turn phone's hold into a booking in Postgres and return the booking's id; then delete the hold and log
        a booked event. BookingError if phone doesn't hold the seat (never held, expired, or someone else's)."""
        raise NotImplementedError("write this")

    def release(self, trip_id, seat, phone):
        """Give up phone's hold on a seat: delete it only if phone holds it, and log a released event then.
        Return True if a hold was released."""
        raise NotImplementedError("write this")

    def free_seats(self, trip_id):
        """The seats on the trip that are neither booked nor held, in order. Find the holds with SCAN (match
        hold:<trip_id>:*), never KEYS."""
        raise NotImplementedError("write this")

    def trip_report(self, trip_id):
        """Kata: {"booked": seats booked (Postgres), "takings": booked seats times the route's fare (Postgres, one
        query), "holds_given_up": how many released events the trip has (MongoDB), "busiest_hour": the UTC hour
        (0-23) with the most held events for the trip, ties to the earlier hour, or None if there are none (a
        MongoDB aggregation)}."""
        raise NotImplementedError("write this")
