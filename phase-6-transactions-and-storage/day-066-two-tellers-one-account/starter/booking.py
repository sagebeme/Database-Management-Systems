"""Day 66 kata: Double Booking.

conn is a PyMySQL connection with autocommit on.
"""


def no_pause():
    pass


def book_seat(conn, trip_id, passenger, pause=no_pause):
    """Book a seat if the trip isn't full: count its bookings, call pause(), and insert one, so that two people
    booking the last seat at the same moment can't both get it. Lock the trip's row while you do it.
    True if booked, False if full."""
    raise NotImplementedError("write this")
