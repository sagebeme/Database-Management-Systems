# Day 86: Embed or Reference?

## The brief

In Phase 4 you normalised: every fact in one place, joined back together when you need it. MongoDB gives you a choice for every relationship. You can **embed** the related data inside the document (the owner inside the vehicle), or **reference** it by id and fetch it separately (the driver from a trip). Get it right and every screen of the app is one fast read. Get it wrong and documents grow without limit, or the same driver's name has to be changed in 10,000 places.

Today you'll model a matatu sacco's fleet: vehicles with their owners, drivers, trips and passenger reviews. You'll make MongoDB check the vehicles' shape, and use `$lookup`, MongoDB's join, where you chose to reference.

## What you'll use

**Embed when** the data:

- belongs to its parent and is read with it ("show the vehicle" always shows the owner);
- is small and *bounded* (a route's dozen stops, a booking's seat numbers);
- isn't shared, or is a snapshot that shouldn't change later (the fare on a receipt).

**Reference when** the data:

- grows without limit (a vehicle's trips: dozens a day, forever);
- is shared by many parents and changes (a driver who drives several vehicles);
- is big, or often read on its own.

A document can't be bigger than **16 MB**, and a document that keeps growing gets slower to read and write long before that.

**The subset pattern** gets both: keep every review in a `reviews` collection, and also embed the newest three in the vehicle, so the vehicle page needs one read. `$push` with `$each` and `$slice` keeps the embedded list short:

```python
{"$push": {"latest_reviews": {"$each": [review], "$slice": -3}}}    # add, then keep the last 3
```

**Schema validation**: "schemaless" doesn't have to mean "anything goes". A `$jsonSchema` validator makes MongoDB refuse documents of the wrong shape:

```python
db.create_collection("vehicles", validator={"$jsonSchema": {
    "bsonType": "object",
    "required": ["_id", "seats"],
    "properties": {
        "seats": {"bsonType": "int", "minimum": 1, "maximum": 70},
        "_id": {"bsonType": "string", "pattern": "^K[A-Z]{2} [0-9]{3}[A-Z]$"},
    },
}})
```

Nested objects get their own `required` and `properties`. Fields you don't mention are allowed.

**`$lookup`** joins in a pipeline:

```python
{"$lookup": {"from": "drivers", "localField": "driver", "foreignField": "_id", "as": "d"}}
```

adds an array `d` of matching drivers to each trip; `{"$unwind": "$d"}` turns it into one object. `{"$size": "$t"}` counts an array, `{"$sum": "$fares"}` adds one up, and `{"$map": {"input": "$t", "as": "x", "in": ...}}` works on each element (refer to it as `"$$x"`).

**References aren't checked.** There are no foreign keys: if you reference driver 99, MongoDB stores it happily. Your code has to check.

## Steps

1. `starter/answers.py`: embed or reference, for six relationships.
2. `starter/fleet.py`: the `VEHICLE_SCHEMA` and `create_vehicles`, then `add_trip`, `add_review` and `trips_with_drivers`.
3. `pytest phase-7-beyond-mysql/day-086-embed-or-reference`

The tests throw thirteen bad vehicles at your validator.

## The kata: The Drivers' Report

In `starter/fleet.py`, write `driver_report(db)`: each driver's trips and total takings, in one pipeline starting from `drivers`, including drivers with no trips.

## When you're stuck

- **A 14.5-seat vehicle gets in**: `"bsonType": "int"` rejects doubles; `"number"` would allow them. Python's `14` is stored as an int.
- **`KDA123A` gets in**: anchor the pattern with `^` and `$`, and put the space in it.
- **`OperationFailure: ... already exists`**: `create_vehicles` makes the collection; insert after it, not before.
- **`latest_reviews` keeps all five**: `$slice: -3` keeps the *last* three; it has to be inside the `$push`, with `$each`.
- **`trips_with_drivers` has `"driver": ["Otieno"]`**: `$lookup` always gives an array. `$unwind` it, then project `"$d.name"`.
- **The kata leaves out Mutua**: start from `drivers` and look up their trips. Starting from trips, a driver with no trips never appears.
