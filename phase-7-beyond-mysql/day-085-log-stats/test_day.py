"""Day 85: Log Stats."""

from collections import Counter
from datetime import datetime
from pathlib import Path

import pymongo
import pytest

from coursekit import load_module

logs_data = load_module(Path(__file__).parent / "logs_data.py")

EXTRA = [
    {"_id": 1001, "ip": "10.0.0.1", "method": "GET", "path": "/status", "status": 200, "ms": 3,
     "at": datetime(2026, 3, 2, 23, 59)},
    {"_id": 1002, "ip": "10.0.0.1", "method": "HEAD", "path": "/status", "status": 503, "ms": 5000,
     "at": datetime(2026, 3, 3, 0, 1)},
    {"_id": 1003, "ip": "10.0.0.2", "method": "POST", "path": "/ussd", "status": 500, "ms": 4000,
     "at": datetime(2026, 3, 3, 0, 2)},
]


@pytest.fixture
def L(target):
    return load_module(target / "log_stats.py")


@pytest.fixture
def db(mongo, mongo_url):
    client = pymongo.MongoClient(mongo_url)
    database = client[mongo.database]
    database.nginx.insert_many(logs_data.logs())
    database.students.insert_many([dict(s) for s in logs_data.STUDENTS])
    yield database
    client.close()


def everything(db):
    return list(db.nginx.find())


def test_report(L, db):
    assert L.report(db.nginx) == ("600 logs\nMethods:\n\tmethod GET: 383\n\tmethod POST: 146\n\tmethod PUT: 21\n"
                                  "\tmethod PATCH: 25\n\tmethod DELETE: 25\n50 status check")
    db.nginx.insert_many([dict(d) for d in EXTRA])
    assert L.report(db.nginx).splitlines()[0] == "603 logs"
    assert L.report(db.nginx).splitlines()[-1] == "51 status check", "HEAD /status isn't a GET"
    assert "\tmethod POST: 147" in L.report(db.nginx).splitlines()


def test_report_on_an_empty_collection(L, db):
    assert L.report(db.empty) == ("0 logs\nMethods:\n\tmethod GET: 0\n\tmethod POST: 0\n\tmethod PUT: 0\n"
                                  "\tmethod PATCH: 0\n\tmethod DELETE: 0\n0 status check")


def expected_top_ips(logs, n):
    return sorted(Counter(d["ip"] for d in logs).items(), key=lambda kv: (-kv[1], kv[0]))[:n]


def test_top_ips(L, db):
    assert L.top_ips(db.nginx, 3) == [("41.90.102.54", 69), ("41.90.192.114", 63), ("41.90.164.98", 60)]
    assert L.top_ips(db.nginx) == expected_top_ips(everything(db), 10)
    db.nginx.insert_many([{"_id": 2000 + i, "ip": "1.1.1.1"} for i in range(69)])
    assert L.top_ips(db.nginx, 2) == [("1.1.1.1", 69), ("41.90.102.54", 69)], "ties by IP"


def test_per_hour(L, db):
    got = L.per_hour(db.nginx)
    assert got[:3] == [(5, 34), (6, 22), (7, 34)] and got[-1] == (21, 40)
    db.nginx.insert_many([dict(d) for d in EXTRA])
    got = L.per_hour(db.nginx)
    assert got == sorted(Counter(d["at"].hour for d in everything(db)).items())
    assert got[0] == (0, 2) and got[-1] == (23, 1)


def test_errors_by_path(L, db):
    got = L.errors_by_path(db.nginx)
    assert got[:2] == [("/login", 13), ("/pay/mpesa", 13)]
    db.nginx.insert_many([dict(d) for d in EXTRA])
    want = Counter(d["path"] for d in everything(db) if d["status"] >= 500)
    assert L.errors_by_path(db.nginx) == sorted(want.items(), key=lambda kv: (-kv[1], kv[0]))
    assert ("/ussd", 1) in L.errors_by_path(db.nginx)


def test_slowest_paths(L, db):
    assert L.slowest_paths(db.nginx) == [("/pay/mpesa", 966.6, 79), ("/bookings/new", 359.3, 85),
                                         ("/login", 207.2, 88)]
    db.nginx.insert_many([dict(d) for d in EXTRA])
    assert L.slowest_paths(db.nginx, 1) == [("/ussd", 4000.0, 1)]
    assert len(L.slowest_paths(db.nginx, 100)) == 8


def test_kata_top_students(L, db):
    got = L.top_students(db.students)
    assert got == [{"_id": 3, "name": "Wairimu", "averageScore": 88.0}, {"_id": 2, "name": "Kamau", "averageScore": 82.0},
                   {"_id": 1, "name": "Achieng", "averageScore": 71.0}, {"_id": 4, "name": "Kiprop", "averageScore": 58.0},
                   {"_id": 5, "name": "Halima", "averageScore": None}]
    db.students.insert_one({"_id": 6, "name": "Barasa", "topics": [{"title": "Maths", "score": 82}]})
    assert [s["name"] for s in L.top_students(db.students)][:3] == ["Wairimu", "Barasa", "Kamau"]
