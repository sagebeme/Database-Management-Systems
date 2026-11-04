"""Day 66 kata: Double Booking.

conn is a PyMySQL connection with autocommit on.
"""


def no_pause():
    pass


def book_seat(conn, trip_id, passenger, pause=no_pause):
    """Book a seat if the trip isn't full: count its bookings, call pause(), and insert one, so that two people
    booking the last seat at the same moment can't both get it. Lock the trip's row while you do it.
    True if booked, False if full."""
    with conn.cursor() as cur:
        cur.execute("START TRANSACTION")
        cur.execute("SELECT seats FROM trips WHERE id = %s FOR UPDATE", (trip_id,))
        (seats,) = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM bookings WHERE trip_id = %s", (trip_id,))
        (taken,) = cur.fetchone()
        if taken >= seats:
            conn.rollback()
            return False
        pause()
        cur.execute("INSERT INTO bookings (trip_id, passenger) VALUES (%s, %s)", (trip_id, passenger))
    conn.commit()
    return True
