"""Day 80: Postgres Superpowers."""

import json

import pytest

SHAKE_UP = """
INSERT INTO routes VALUES ('9', '{Kencom,Westlands,"Lavington"}'), ('34', '{}');
INSERT INTO trips VALUES
    (9, '9', '{"driver": "Achieng", "cashless": true, "fares": [80, 80, 80, 80, 80, 80]}'),
    (10, '46', '{"driver": "Barasa", "cashless": "yes", "fares": [70]}'),
    (11, '58', '{"driver": "Halima", "cashless": false, "fares": [60], "extra": {"cashless": true}}');
INSERT INTO notices VALUES
    (7, '2026-03-25', 'ROADS CLOSE early on Sunday for the marathon.'),
    (8, '2026-03-26', 'The office will close at noon.'),
    (9, '2026-03-27', 'Ngong Road: the new lane is now open.');
"""


@pytest.fixture
def pg(postgres, day):
    postgres.load(day / "setup.sql")
    return postgres


def same_as_solution(pg, target, day, name):
    got = pg.run_file(target / name).check()
    want = pg.run_file(day / "solution" / name).check()
    assert got.columns == want.columns
    assert got.rows == want.rows
    return got


def test_cashless_trips(pg, target, day):
    got = pg.run_file(target / "0-cashless_trips.sql").check()
    assert got.columns == ["id", "route", "driver"]
    assert got.rows == [("1", "46", "Otieno"), ("3", "111", "Chebet"), ("4", "125", "Mutua"), ("6", "58", "Otieno"),
                        ("7", "237", "Wanjiru")]
    pg.run(SHAKE_UP).check()
    got = same_as_solution(pg, target, day, "0-cashless_trips.sql")
    assert ("10", "46", "Barasa") not in got.rows, '"yes" is a string, not true'
    assert ("11", "58", "Halima") not in got.rows, "only a top-level cashless counts"


def test_takings(pg, target, day):
    got = pg.run_file(target / "1-takings.sql").check()
    assert got.columns == ["id", "passengers", "takings"]
    assert got.rows == [("1", "3", "190"), ("2", "4", "280"), ("3", "2", "180"), ("4", "3", "360"), ("5", "0", "0"),
                        ("6", "5", "300"), ("7", "2", "300"), ("8", "1", "100")]
    pg.run(SHAKE_UP).check()
    same_as_solution(pg, target, day, "1-takings.sql")


def test_details_index(pg, target):
    pg.run_file(target / "2-details_index.sql").check()
    rows = pg.run("SELECT indexdef FROM pg_indexes WHERE indexname = 'idx_trips_details';").check().rows
    assert rows and "USING gin (details)" in rows[0][0], "a GIN index on details"
    plan = pg.run("SET enable_seqscan = off; EXPLAIN SELECT id FROM trips WHERE details @> '{\"cashless\": true}';")
    assert "idx_trips_details" in plan.check().stdout, "containment searches should be able to use it"


def test_via_westlands(pg, target, day):
    got = pg.run_file(target / "3-via_westlands.sql").check()
    assert got.columns == ["number", "stop_count"]
    assert got.rows == [("105", "4"), ("46", "4")]
    pg.run(SHAKE_UP).check()
    assert ("9", "3") in same_as_solution(pg, target, day, "3-via_westlands.sql").rows


def test_busiest_stops(pg, target, day):
    got = pg.run_file(target / "4-busiest_stops.sql").check()
    assert got.columns == ["stop", "routes"]
    assert got.rows[:4] == [("Kencom", "2"), ("Odeon", "2"), ("Railways", "2"), ("Westlands", "2")]
    assert len(got.rows) == 19
    pg.run(SHAKE_UP).check()
    got = same_as_solution(pg, target, day, "4-busiest_stops.sql")
    assert got.rows[:2] == [("Kencom", "3"), ("Westlands", "3")]


def test_closures(pg, target, day):
    got = pg.run_file(target / "5-closures.sql").check()
    assert got.columns == ["id", "posted"]
    assert got.rows == [("1", "2026-03-02"), ("5", "2026-03-14")]
    pg.run(SHAKE_UP).check()
    got = same_as_solution(pg, target, day, "5-closures.sql")
    assert [r[0] for r in got.rows] == ["1", "5", "7"], "ROADS CLOSE counts; an office closing doesn't; open doesn't"


def test_kata(pg, target, day):
    got = pg.run_file(target / "kata.sql").check()
    assert got.columns == ["number", "trips"]
    trips = {n: json.loads(t) for n, t in got.rows}
    assert trips["125"] == [{"id": 4, "driver": "Mutua"}, {"id": 8, "driver": "Kiprop"}]
    assert trips["105"] == [{"id": 5, "driver": "Njeri"}]
    pg.run(SHAKE_UP).check()
    same_as_solution(pg, target, day, "kata.sql")
    trips = {n: json.loads(t) for n, t in pg.run_file(target / "kata.sql").check().rows}
    assert trips["34"] == [], "a route with no trips gets an empty array, not NULL or [null]"
    query = "\n".join(line for line in (target / "kata.sql").read_text().splitlines()
                      if not line.lstrip().startswith("--")).strip().rstrip(";")
    assert pg.run(f"SELECT pg_typeof(trips)::text FROM ({query}\n) AS k LIMIT 1;").check().rows == [("jsonb",)], \
        "trips should be jsonb"
