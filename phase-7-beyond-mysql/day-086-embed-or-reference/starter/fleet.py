"""Day 86: embed or reference? A matatu sacco's fleet in MongoDB.

`db` is a pymongo Database. The collections:

    vehicles  {"_id": "KDA 123A", "seats": 14, "owner": {"name": ..., "phone": ...},   <- the owner is embedded
               "latest_reviews": [{"stars": 4, "text": ...}, ...]}                       <- at most 3, newest last
    drivers   {"_id": 1, "name": "Otieno", "licence": "DL-0001"}
    trips     {"_id": ..., "vehicle": "KDA 123A", "driver": 1, "stops": ["Kencom", ...], "fares": [70, 70]}
              <- vehicle and driver are references; stops are embedded
    reviews   {"_id": ..., "vehicle": "KDA 123A", "stars": 4, "text": ...}             <- every review, forever
"""

VEHICLE_SCHEMA = None  # write the $jsonSchema here and use it in create_vehicles


def create_vehicles(db):
    """Create the vehicles collection with a $jsonSchema validator, so MongoDB itself refuses a vehicle whose
    plate (_id) isn't like "KDA 123A", whose seats isn't a whole number from 1 to 70, or whose owner isn't an
    object with a name and a phone like "254711000001"."""
    raise NotImplementedError("write this")


def add_trip(db, plate, driver_id, stops, fares):
    """Record a trip, referring to the vehicle and the driver by their _id. ValueError if either doesn't exist.
    Return the trip's _id."""
    raise NotImplementedError("write this")


def add_review(db, plate, stars, text):
    """Keep every review in reviews, and the newest 3 embedded in the vehicle's latest_reviews (the subset
    pattern: the vehicle page shows 3 without a second query; the rest are a click away)."""
    raise NotImplementedError("write this")


def trips_with_drivers(db):
    """Every trip as {"trip": _id, "vehicle": plate, "driver": the driver's name}, by trip _id. One aggregation,
    with $lookup."""
    raise NotImplementedError("write this")


def driver_report(db):
    """Kata: for every driver, including ones with no trips: {"driver": name, "trips": how many, "takings": the
    sum of all their trips' fares}. Most takings first, ties by name. One aggregation, starting from drivers."""
    raise NotImplementedError("write this")
