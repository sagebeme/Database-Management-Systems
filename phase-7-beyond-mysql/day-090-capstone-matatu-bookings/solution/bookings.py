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
        cached = self.r.get("cache:routes")
        if cached is not None:
            return [tuple(r) for r in json.loads(cached)]
        with self.pg.cursor() as cur:
            cur.execute("SELECT number, fare FROM routes ORDER BY number")
            rows = cur.fetchall()
        self.r.set("cache:routes", json.dumps(rows), ex=CACHE_SECONDS)
        return rows

    def set_fare(self, number, fare):
        """Change a route's fare in Postgres, drop the cached route list so nobody sees the old fare, and log a
        fare_changed event. BookingError if there's no such route."""
        with self.pg.cursor() as cur:
            cur.execute("UPDATE routes SET fare = %s WHERE number = %s", (fare, number))
            if cur.rowcount == 0:
                raise BookingError(f"no route {number}")
        self.r.delete("cache:routes")
        self._log("fare_changed", route=number, fare=fare)

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
        seats = self._seats(trip_id)
        if not 1 <= seat <= seats:
            raise BookingError(f"trip {trip_id} has seats 1 to {seats}")
        if seat in self._booked(trip_id):
            raise BookingError(f"seat {seat} is booked")
        key = f"hold:{trip_id}:{seat}"
        if not self.r.set(key, phone, nx=True, ex=HOLD_SECONDS):
            holder = self.r.get(key)
            if holder is None or holder.decode() != phone:
                raise BookingError(f"seat {seat} is held by someone else")
            self.r.expire(key, HOLD_SECONDS)
        self._log("held", trip=trip_id, seat=seat, phone=phone)

    def confirm(self, trip_id, seat, phone):
        """Turn phone's hold into a booking in Postgres and return the booking's id; then delete the hold and log
        a booked event. BookingError if phone doesn't hold the seat (never held, expired, or someone else's)."""
        holder = self.r.get(f"hold:{trip_id}:{seat}")
        if holder is None or holder.decode() != phone:
            raise BookingError(f"{phone} doesn't hold seat {seat}")
        with self.pg.cursor() as cur:
            cur.execute("INSERT INTO bookings (trip_id, seat, phone) VALUES (%s, %s, %s) RETURNING id",
                        (trip_id, seat, phone))
            booking = cur.fetchone()[0]
        self.r.delete(f"hold:{trip_id}:{seat}")
        self._log("booked", trip=trip_id, seat=seat, phone=phone)
        return booking

    def release(self, trip_id, seat, phone):
        """Give up phone's hold on a seat: delete it only if phone holds it, and log a released event then.
        Return True if a hold was released."""
        key = f"hold:{trip_id}:{seat}"
        holder = self.r.get(key)
        if holder is None or holder.decode() != phone:
            return False
        self.r.delete(key)
        self._log("released", trip=trip_id, seat=seat, phone=phone)
        return True

    def free_seats(self, trip_id):
        """The seats on the trip that are neither booked nor held, in order. Find the holds with SCAN (match
        hold:<trip_id>:*), never KEYS."""
        held = {int(k.decode().rsplit(":", 1)[1]) for k in self.r.scan_iter(match=f"hold:{trip_id}:*")}
        taken = held | self._booked(trip_id)
        return [s for s in range(1, self._seats(trip_id) + 1) if s not in taken]

    def trip_report(self, trip_id):
        """Kata: {"booked": seats booked (Postgres), "takings": booked seats times the route's fare (Postgres, one
        query), "holds_given_up": how many released events the trip has (MongoDB), "busiest_hour": the UTC hour
        (0-23) with the most held events for the trip, ties to the earlier hour, or None if there are none (a
        MongoDB aggregation)}."""
        with self.pg.cursor() as cur:
            cur.execute("""SELECT count(b.id), COALESCE(count(b.id) * r.fare, 0)
                           FROM trips t JOIN routes r ON r.number = t.route
                           LEFT JOIN bookings b ON b.trip_id = t.id
                           WHERE t.id = %s GROUP BY r.fare""", (trip_id,))
            row = cur.fetchone()
        if row is None:
            raise BookingError(f"no trip {trip_id}")
        busiest = list(self.events.aggregate([
            {"$match": {"type": "held", "trip": trip_id}},
            {"$group": {"_id": {"$hour": "$at"}, "n": {"$sum": 1}}},
            {"$sort": {"n": -1, "_id": 1}},
            {"$limit": 1},
        ]))
        return {
            "booked": row[0],
            "takings": row[1],
            "holds_given_up": self.events.count_documents({"type": "released", "trip": trip_id}),
            "busiest_hour": busiest[0]["_id"] if busiest else None,
        }
