"""Day 85: log stats and aggregation pipelines.

`nginx` is a pymongo Collection of web server logs:
    {"_id": 1, "ip": "41.90.12.7", "method": "GET", "path": "/routes", "status": 200, "ms": 73,
     "at": datetime(2026, 3, 2, 5, 14)}
"""

METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def report(nginx):
    """The summary, exactly like this (a tab before each "method"):

    600 logs
    Methods:
    \tmethod GET: 383
    \tmethod POST: 146
    \tmethod PUT: 21
    \tmethod PATCH: 25
    \tmethod DELETE: 25
    50 status check

    where the last line counts GET requests to /status. Return it as one string, lines joined with "\\n"."""
    lines = [f"{nginx.count_documents({})} logs", "Methods:"]
    lines += [f"\tmethod {m}: {nginx.count_documents({'method': m})}" for m in METHODS]
    lines.append(f"{nginx.count_documents({'method': 'GET', 'path': '/status'})} status check")
    return "\n".join(lines)


def top_ips(nginx, n=10):
    """The n IPs with the most requests: [(ip, requests)], most first, ties by IP. One aggregation."""
    pipeline = [
        {"$group": {"_id": "$ip", "requests": {"$sum": 1}}},
        {"$sort": {"requests": -1, "_id": 1}},
        {"$limit": n},
    ]
    return [(d["_id"], d["requests"]) for d in nginx.aggregate(pipeline)]


def per_hour(nginx):
    """Requests in each hour of the day that has any: [(hour, requests)], by hour. Hours are 0 to 23."""
    pipeline = [
        {"$group": {"_id": {"$hour": "$at"}, "requests": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]
    return [(d["_id"], d["requests"]) for d in nginx.aggregate(pipeline)]


def errors_by_path(nginx):
    """For each path with at least one server error (status 500 or more): [(path, errors)], most first, ties by
    path."""
    pipeline = [
        {"$match": {"status": {"$gte": 500}}},
        {"$group": {"_id": "$path", "errors": {"$sum": 1}}},
        {"$sort": {"errors": -1, "_id": 1}},
    ]
    return [(d["_id"], d["errors"]) for d in nginx.aggregate(pipeline)]


def slowest_paths(nginx, n=3):
    """The n paths with the highest average response time: [(path, average_ms rounded to 1 decimal place,
    requests)], slowest first."""
    pipeline = [
        {"$group": {"_id": "$path", "avg": {"$avg": "$ms"}, "requests": {"$sum": 1}}},
        {"$sort": {"avg": -1, "_id": 1}},
        {"$limit": n},
    ]
    return [(d["_id"], round(d["avg"], 1), d["requests"]) for d in nginx.aggregate(pipeline)]


def top_students(students):
    """Kata: every student as {"_id", "name", "averageScore"}, best average first. A student's average is over
    their topics' scores; a student with no topics has averageScore None and comes last. Ties by name."""
    pipeline = [
        {"$project": {"name": 1, "averageScore": {"$avg": "$topics.score"}}},
        {"$sort": {"averageScore": -1, "name": 1}},
    ]
    return list(students.aggregate(pipeline))
