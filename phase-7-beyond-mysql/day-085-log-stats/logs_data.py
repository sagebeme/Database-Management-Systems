"""The same 600 made-up web server logs every time, from the matatu booking API's busiest Monday.

    python phase-7-beyond-mysql/day-085-log-stats/logs_data.py      loads them into logs.nginx (and students)
"""

import random
from datetime import datetime, timedelta

METHODS = ["GET"] * 12 + ["POST"] * 5 + ["PUT", "PATCH", "DELETE"]
PATHS = ["/routes", "/routes/46", "/bookings", "/bookings/new", "/status", "/login", "/pay/mpesa"]
SLOW = {"/pay/mpesa": 900, "/bookings/new": 300, "/login": 150}


def logs():
    rng = random.Random(85)
    ips = [f"41.90.{rng.randrange(256)}.{rng.randrange(256)}" for _ in range(25)]
    start = datetime(2026, 3, 2, 5, 0)
    out = []
    for i in range(600):
        path = rng.choice(PATHS)
        status = rng.choices([200, 201, 302, 400, 401, 404, 500, 503], [60, 8, 5, 6, 5, 6, 6, 4])[0]
        out.append({
            "_id": i + 1,
            "ip": rng.choice(ips[:5]) if rng.random() < 0.4 else rng.choice(ips),
            "method": rng.choice(METHODS),
            "path": path,
            "status": status,
            "ms": SLOW.get(path, 40) + rng.randrange(120),
            "at": start + timedelta(minutes=rng.randrange(17 * 60)),
        })
    return out


STUDENTS = [
    {"_id": 1, "name": "Achieng", "topics": [{"title": "Maths", "score": 78}, {"title": "Chemistry", "score": 64}]},
    {"_id": 2, "name": "Kamau", "topics": [{"title": "Maths", "score": 91}, {"title": "Physics", "score": 85},
                                          {"title": "Chemistry", "score": 70}]},
    {"_id": 3, "name": "Wairimu", "topics": [{"title": "Biology", "score": 88}]},
    {"_id": 4, "name": "Kiprop", "topics": [{"title": "Maths", "score": 55}, {"title": "Geography", "score": 61}]},
    {"_id": 5, "name": "Halima", "topics": []},
]

if __name__ == "__main__":
    from pymongo import MongoClient

    db = MongoClient("mongodb://127.0.0.1:27018").logs
    db.nginx.drop()
    db.nginx.insert_many(logs())
    db.students.drop()
    db.students.insert_many(STUDENTS)
    print(f"{db.nginx.count_documents({})} logs and {db.students.count_documents({})} students in the logs database")
