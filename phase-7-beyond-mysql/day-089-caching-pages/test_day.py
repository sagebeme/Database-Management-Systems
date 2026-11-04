"""Day 89: Caching Pages."""

import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from coursekit import load_module


@pytest.fixture
def web(target):
    return load_module(target / "web.py")


@pytest.fixture
def rides(target):
    return load_module(target / "rides.py")


@pytest.fixture
def site():
    """A tiny local web server that counts its visits: each page says how many times it has been fetched."""
    hits = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            hits[self.path] = hits.get(self.path, 0) + 1
            body = f"<h1>Ratiba {self.path}</h1><p>fetch {hits[self.path]}</p>".encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}", hits
    server.shutdown()


def test_get_page_caches(web, redis_db, site):
    base, hits = site
    url = f"{base}/routes/46"
    assert web.get_page(redis_db, url) == "<h1>Ratiba /routes/46</h1><p>fetch 1</p>"
    assert web.get_page(redis_db, url) == "<h1>Ratiba /routes/46</h1><p>fetch 1</p>", "the second one is cached"
    assert hits == {"/routes/46": 1}
    assert redis_db.get(f"count:{url}") == b"2", "count every call, cached or not"
    assert 8 <= redis_db.ttl(f"cached:{url}") <= 10


def test_get_page_expires(web, redis_db, site):
    base, hits = site
    url = f"{base}/routes/111"
    web.get_page(redis_db, url, seconds=1)
    time.sleep(1.2)
    assert web.get_page(redis_db, url, seconds=1).endswith("fetch 2</p>")
    assert redis_db.get(f"count:{url}") == b"2"


def test_get_page_keeps_urls_apart(web, redis_db, site):
    base, hits = site
    web.get_page(redis_db, f"{base}/a")
    web.get_page(redis_db, f"{base}/b")
    web.get_page(redis_db, f"{base}/a")
    assert hits == {"/a": 1, "/b": 1}
    assert redis_db.get(f"count:{base}/a") == b"2" and redis_db.get(f"count:{base}/b") == b"1"


def test_queue(rides, redis_db):
    assert rides.next_ride(redis_db) is None
    for phone in ("254711000001", "254722000002", "254733000003"):
        rides.request_ride(redis_db, phone)
    assert rides.next_ride(redis_db) == "254711000001", "first come, first served"
    rides.request_ride(redis_db, "254744000004")
    assert [rides.next_ride(redis_db) for _ in range(4)] == ["254722000002", "254733000003", "254744000004", None]


def test_riders_and_regulars(rides, redis_db):
    days = {
        "2026-03-02": ["254711000001", "254722000002", "254733000003", "254711000001"],
        "2026-03-03": ["254711000001", "254733000003"],
        "2026-03-04": ["254733000003", "254744000004", "254711000001"],
    }
    for day, phones in days.items():
        for phone in phones:
            rides.rode(redis_db, day, phone)
    assert rides.riders(redis_db, "2026-03-02") == 3, "twice in a day counts once"
    assert rides.riders(redis_db, "2026-03-09") == 0
    assert rides.regulars(redis_db, list(days)) == ["254711000001", "254733000003"]
    assert rides.regulars(redis_db, ["2026-03-04"]) == ["254711000001", "254733000003", "254744000004"]
    assert rides.regulars(redis_db, ["2026-03-02", "2026-03-09"]) == []
    assert rides.regulars(redis_db, []) == []


def test_seats(rides, redis_db):
    assert rides.book_seat(redis_db, "T46-0700", 1, "254711000001") is True
    assert rides.book_seat(redis_db, "T46-0700", 1, "254722000002") is False, "seat 1 is taken"
    assert rides.book_seat(redis_db, "T46-0700", 14, "254722000002") is True
    assert rides.book_seat(redis_db, "T46-0800", 1, "254733000003") is True, "another trip, another hash"
    assert rides.seat_map(redis_db, "T46-0700") == {1: "254711000001", 14: "254722000002"}
    assert rides.seat_map(redis_db, "T99-0000") == {}


def test_seats_under_pressure(rides, redis_db, target):
    import redis as redis_lib
    url = redis_db.connection_pool.connection_kwargs
    gate = threading.Barrier(8)
    won = []

    def grab(n):
        r = redis_lib.Redis(host=url["host"], port=url["port"], db=url.get("db", 0))
        gate.wait()
        if rides.book_seat(r, "T46-0900", 7, f"25470000000{n}"):
            won.append(n)

    threads = [threading.Thread(target=grab, args=(n,)) for n in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(won) == 1, "eight people tap seat 7 at once: exactly one gets it"


def test_leaderboard(rides, redis_db):
    assert rides.add_points(redis_db, "Otieno", 30) == 30
    assert rides.add_points(redis_db, "Chebet", 45) == 45
    assert rides.add_points(redis_db, "Otieno", 20) == 50
    rides.add_points(redis_db, "Mutua", 10)
    assert rides.top_drivers(redis_db, 2) == [("Otieno", 50), ("Chebet", 45)]
    assert rides.top_drivers(redis_db, 10) == [("Otieno", 50), ("Chebet", 45), ("Mutua", 10)]


def test_kata_sliding_window(rides, redis_db):
    phone = "254711000001"
    got = [rides.allowed(redis_db, phone, 3, 60, now) for now in (1000, 1010, 1020, 1030)]
    assert got == [True, True, True, False]
    assert redis_db.zcard(f"requests:{phone}") == 3, "a refused request isn't recorded"
    assert rides.allowed(redis_db, phone, 3, 60, 1059) is False
    assert rides.allowed(redis_db, phone, 3, 60, 1060) is True, "1000 is now a full window old"
    assert rides.allowed(redis_db, phone, 3, 60, 1061) is False
    assert rides.allowed(redis_db, phone, 3, 60, 1071) is True
    assert 55 <= redis_db.ttl(f"requests:{phone}") <= 60
    assert rides.allowed(redis_db, "254722000002", 1, 60, 1071) is True, "every phone has its own window"


def test_kata_no_burst_at_the_edge(rides, redis_db):
    phone = "254711000001"
    assert all(rides.allowed(redis_db, phone, 5, 60, t) for t in (55, 56, 57, 58, 59))
    assert not any(rides.allowed(redis_db, phone, 5, 60, t) for t in (61, 62, 63)), \
        "a fixed window starting at 60 would let 5 more through here; a sliding one doesn't"
