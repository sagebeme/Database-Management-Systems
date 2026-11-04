"""Day 86: embed or reference? A matatu sacco's fleet in MongoDB.

`db` is a pymongo Database. The collections:

    vehicles  {"_id": "KDA 123A", "seats": 14, "owner": {"name": ..., "phone": ...},   <- the owner is embedded
               "latest_reviews": [{"stars": 4, "text": ...}, ...]}                       <- at most 3, newest last
    drivers   {"_id": 1, "name": "Otieno", "licence": "DL-0001"}
    trips     {"_id": ..., "vehicle": "KDA 123A", "driver": 1, "stops": ["Kencom", ...], "fares": [70, 70]}
              <- vehicle and driver are references; stops are embedded
    reviews   {"_id": ..., "vehicle": "KDA 123A", "stars": 4, "text": ...}             <- every review, forever
"""

VEHICLE_SCHEMA = {
    "bsonType": "object",
    "required": ["_id", "seats", "owner"],
    "properties": {
        "_id": {"bsonType": "string", "pattern": "^K[A-Z]{2} [0-9]{3}[A-Z]$"},
        "seats": {"bsonType": "int", "minimum": 1, "maximum": 70},
        "owner": {
            "bsonType": "object",
            "required": ["name", "phone"],
            "properties": {
                "name": {"bsonType": "string", "minLength": 1},
                "phone": {"bsonType": "string", "pattern": "^2547[0-9]{8}$"},
            },
        },
    },
}


def create_vehicles(db):
    """Create the vehicles collection with a $jsonSchema validator, so MongoDB itself refuses a vehicle whose
    plate (_id) isn't like "KDA 123A", whose seats isn't a whole number from 1 to 70, or whose owner isn't an
    object with a name and a phone like "254711000001"."""
    db.create_collection("vehicles", validator={"$jsonSchema": VEHICLE_SCHEMA})


def add_trip(db, plate, driver_id, stops, fares):
    """Record a trip, referring to the vehicle and the driver by their _id. ValueError if either doesn't exist.
    Return the trip's _id."""
    if db.vehicles.count_documents({"_id": plate}, limit=1) == 0:
        raise ValueError(f"no vehicle {plate}")
    if db.drivers.count_documents({"_id": driver_id}, limit=1) == 0:
        raise ValueError(f"no driver {driver_id}")
    return db.trips.insert_one({"vehicle": plate, "driver": driver_id, "stops": list(stops),
                                "fares": list(fares)}).inserted_id


def add_review(db, plate, stars, text):
    """Keep every review in reviews, and the newest 3 embedded in the vehicle's latest_reviews (the subset
    pattern: the vehicle page shows 3 without a second query; the rest are a click away)."""
    review = {"stars": stars, "text": text}
    db.reviews.insert_one({"vehicle": plate, **review})
    db.vehicles.update_one({"_id": plate}, {"$push": {"latest_reviews": {"$each": [review], "$slice": -3}}})


def trips_with_drivers(db):
    """Every trip as {"trip": _id, "vehicle": plate, "driver": the driver's name}, by trip _id. One aggregation,
    with $lookup."""
    pipeline = [
        {"$sort": {"_id": 1}},
        {"$lookup": {"from": "drivers", "localField": "driver", "foreignField": "_id", "as": "d"}},
        {"$unwind": "$d"},
        {"$project": {"_id": 0, "trip": "$_id", "vehicle": 1, "driver": "$d.name"}},
    ]
    return list(db.trips.aggregate(pipeline))


def driver_report(db):
    """Kata: for every driver, including ones with no trips: {"driver": name, "trips": how many, "takings": the
    sum of all their trips' fares}. Most takings first, ties by name. One aggregation, starting from drivers."""
    pipeline = [
        {"$lookup": {"from": "trips", "localField": "_id", "foreignField": "driver", "as": "t"}},
        {"$project": {
            "_id": 0,
            "driver": "$name",
            "trips": {"$size": "$t"},
            "takings": {"$sum": {"$map": {"input": "$t", "as": "trip", "in": {"$sum": "$$trip.fares"}}}},
        }},
        {"$sort": {"takings": -1, "driver": 1}},
    ]
    return list(db.drivers.aggregate(pipeline))
