"""Day 86: Embed or Reference?"""

import pymongo
import pytest
from pymongo.errors import WriteError

from coursekit import load_module

OWNER = {"name": "Wanjiku Kamau", "phone": "254711000001"}


@pytest.fixture
def f(target):
    return load_module(target / "fleet.py")


@pytest.fixture
def db(mongo, mongo_url):
    client = pymongo.MongoClient(mongo_url)
    yield client[mongo.database]
    client.close()


@pytest.fixture
def fleet(f, db):
    """Vehicles made with your create_vehicles, and three drivers."""
    f.create_vehicles(db)
    db.vehicles.insert_many([
        {"_id": "KDA 123A", "seats": 14, "owner": OWNER},
        {"_id": "KCB 456B", "seats": 33, "owner": {"name": "Otieno Ochieng", "phone": "254722000002"}},
    ])
    db.drivers.insert_many([{"_id": 1, "name": "Otieno", "licence": "DL-0001"},
                            {"_id": 2, "name": "Chebet", "licence": "DL-0002"},
                            {"_id": 3, "name": "Mutua", "licence": "DL-0003"}])
    return db


def test_create_vehicles_accepts_good_ones(f, db):
    f.create_vehicles(db)
    db.vehicles.insert_one({"_id": "KDA 123A", "seats": 14, "owner": OWNER})
    db.vehicles.insert_one({"_id": "KBZ 010D", "seats": 70, "owner": OWNER, "colour": "maroon"})
    assert db.vehicles.count_documents({}) == 2
    assert "$jsonSchema" in db.command("listCollections", filter={"name": "vehicles"})["cursor"]["firstBatch"][0][
        "options"]["validator"]


@pytest.mark.parametrize("vehicle", [
    {"_id": "KDA123A", "seats": 14, "owner": OWNER},
    {"_id": "kda 123a", "seats": 14, "owner": OWNER},
    {"_id": "UAA 123A", "seats": 14, "owner": OWNER},
    {"_id": "KDA 123A", "seats": 0, "owner": OWNER},
    {"_id": "KDA 123A", "seats": 71, "owner": OWNER},
    {"_id": "KDA 123A", "seats": 14.5, "owner": OWNER},
    {"_id": "KDA 123A", "seats": "14", "owner": OWNER},
    {"_id": "KDA 123A", "owner": OWNER},
    {"_id": "KDA 123A", "seats": 14},
    {"_id": "KDA 123A", "seats": 14, "owner": "Wanjiku Kamau"},
    {"_id": "KDA 123A", "seats": 14, "owner": {"name": "Wanjiku Kamau"}},
    {"_id": "KDA 123A", "seats": 14, "owner": {"name": "Wanjiku Kamau", "phone": "0711000001"}},
    {"_id": "KDA 123A", "seats": 14, "owner": {"name": "", "phone": "254711000001"}},
])
def test_create_vehicles_refuses_bad_ones(f, db, vehicle):
    f.create_vehicles(db)
    with pytest.raises(WriteError):
        db.vehicles.insert_one(vehicle)


def test_add_trip(f, fleet):
    first = f.add_trip(fleet, "KDA 123A", 1, ["Kencom", "Westlands"], [70, 70, 50])
    trip = fleet.trips.find_one({"_id": first})
    assert {k: trip[k] for k in ("vehicle", "driver", "stops", "fares")} == {
        "vehicle": "KDA 123A", "driver": 1, "stops": ["Kencom", "Westlands"], "fares": [70, 70, 50]}
    assert f.add_trip(fleet, "KCB 456B", 1, ("Odeon",), ()) != first
    with pytest.raises(ValueError):
        f.add_trip(fleet, "KXX 999X", 1, [], [])
    with pytest.raises(ValueError):
        f.add_trip(fleet, "KDA 123A", 99, [], [])
    assert fleet.trips.count_documents({}) == 2


def test_add_review_keeps_three(f, fleet):
    for n in range(1, 6):
        f.add_review(fleet, "KDA 123A", n, f"review {n}")
    vehicle = fleet.vehicles.find_one({"_id": "KDA 123A"})
    assert vehicle["latest_reviews"] == [{"stars": 3, "text": "review 3"}, {"stars": 4, "text": "review 4"},
                                         {"stars": 5, "text": "review 5"}]
    assert fleet.reviews.count_documents({"vehicle": "KDA 123A"}) == 5
    assert "latest_reviews" not in fleet.vehicles.find_one({"_id": "KCB 456B"})
    f.add_review(fleet, "KCB 456B", 2, "loud music")
    assert fleet.vehicles.find_one({"_id": "KCB 456B"})["latest_reviews"] == [{"stars": 2, "text": "loud music"}]


def test_trips_with_drivers(f, fleet):
    fleet.trips.insert_many([{"_id": 10, "vehicle": "KDA 123A", "driver": 2, "fares": [70]},
                             {"_id": 5, "vehicle": "KCB 456B", "driver": 1, "fares": []},
                             {"_id": 7, "vehicle": "KDA 123A", "driver": 1, "fares": [70, 70]}])
    assert f.trips_with_drivers(fleet) == [
        {"trip": 5, "vehicle": "KCB 456B", "driver": "Otieno"},
        {"trip": 7, "vehicle": "KDA 123A", "driver": "Otieno"},
        {"trip": 10, "vehicle": "KDA 123A", "driver": "Chebet"}]
    fleet.drivers.update_one({"_id": 1}, {"$set": {"name": "Otieno O."}})
    assert f.trips_with_drivers(fleet)[0]["driver"] == "Otieno O.", "a reference: change the name once, see it everywhere"


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.A_VEHICLES_OWNER_DETAILS, a.A_ROUTES_LIST_OF_STOPS, a.A_VEHICLES_TRIPS,
            a.DRIVERS_WHO_DRIVE_MANY_VEHICLES, a.A_BOOKINGS_SEAT_NUMBERS, a.EVERY_COMMENT_ON_A_POPULAR_ROUTE] == [
        "embed", "embed", "reference", "reference", "embed", "reference"]
    assert a.DOCUMENT_LIMIT_MB == 16


def test_kata_driver_report(f, fleet):
    fleet.trips.insert_many([{"_id": 1, "vehicle": "KDA 123A", "driver": 1, "fares": [70, 70, 50]},
                             {"_id": 2, "vehicle": "KCB 456B", "driver": 2, "fares": [100, 100]},
                             {"_id": 3, "vehicle": "KDA 123A", "driver": 1, "fares": []},
                             {"_id": 4, "vehicle": "KDA 123A", "driver": 2, "fares": [40]}])
    assert f.driver_report(fleet) == [{"driver": "Chebet", "trips": 2, "takings": 240},
                                      {"driver": "Otieno", "trips": 2, "takings": 190},
                                      {"driver": "Mutua", "trips": 0, "takings": 0}]
    fleet.drivers.insert_one({"_id": 4, "name": "Akinyi"})
    fleet.trips.insert_one({"_id": 5, "vehicle": "KDA 123A", "driver": 3, "fares": [240]})
    assert [r["driver"] for r in f.driver_report(fleet)] == ["Chebet", "Mutua", "Otieno", "Akinyi"]
