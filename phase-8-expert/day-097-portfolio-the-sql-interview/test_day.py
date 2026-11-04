"""Day 97: Portfolio: The SQL Interview.

Each answer is checked against the reference answer twice: on the data in setup.sql, and again after
the data changes (new trips, a deleted range, a banned rider...), so an answer that only fits today's
rows fails."""

import pytest

QUESTIONS = [f"q{n:02d}" for n in range(1, 21)] + ["kata"]

CHANGES = """
INSERT INTO riders (id, name, phone, referred_by, banned) VALUES
    (41, 'Zawadi Mutua', (SELECT phone FROM riders WHERE id = 7), 39, false),
    (42, 'Neema Ali', '254799000111', 41, false);
UPDATE riders SET banned = true WHERE id = 2;
INSERT INTO drivers (id, name, county, vehicle) VALUES (13, 'Kevin Odera', 'Kisii', 'car'), (14, 'Rose Moraa', 'Kisii', 'boda'),
    (15, 'Lucy Wangari', 'Kisii', 'tuktuk');
INSERT INTO trips (id, rider_id, driver_id, requested_at, fare, status, payment, rating) VALUES
    (3101, 41, 3, '2026-01-02 07:00', 990, 'completed', 'mpesa', 1),
    (3102, 41, 3, '2026-01-03 07:10', 990, 'completed', 'mpesa', 1),
    (3103, 41, 13, '2026-01-04 07:20', 980, 'completed', 'cash', 5),
    (3104, 41, 14, '2026-01-04 07:45', 120, 'completed', 'cash', NULL),
    (3105, 42, 13, '2026-04-30 23:30', 75, 'cancelled', 'cash', NULL),
    (3106, 42, 13, '2026-05-01 00:10', 75, 'completed', 'cash', 2),
    (3107, 41, 3, '2026-01-02 07:00', 990, 'completed', 'mpesa', NULL),
    (3108, 7, 14, '2026-01-01 06:00', 40, 'cancelled', 'mpesa', NULL),
    (3109, 13, 14, '2026-01-06 09:00', 40, 'cancelled', 'mpesa', NULL);
DELETE FROM trips WHERE id BETWEEN 1 AND 3 OR id BETWEEN 500 AND 520;
UPDATE trips SET status = 'cancelled' WHERE id IN (2003, 2004, 133, 363);
UPDATE trips SET fare = 495 WHERE id IN (961, 1191);
"""


@pytest.fixture
def boda(postgres, day):
    postgres.load(day / "setup.sql")
    return postgres


def compare(db, target, day, name):
    mine = db.run_file(target / f"{name}.sql")
    assert mine.ok, f"{name}.sql failed: {mine.stderr}"
    want = db.run_file(day / "solution" / f"{name}.sql").check()
    assert mine.columns == want.columns, f"{name}: the columns should be {want.columns}"
    assert len(mine.rows) == len(want.rows), f"{name}: expected {len(want.rows)} rows, got {len(mine.rows)}"
    for got, expected in zip(mine.rows, want.rows):
        assert got == expected, f"{name}: first wrong row is {got}, expected {expected}"


@pytest.mark.parametrize("name", QUESTIONS)
def test_question(boda, target, day, name):
    compare(boda, target, day, name)
    boda.run(CHANGES).check()
    compare(boda, target, day, name)


@pytest.mark.passes_on_starter
def test_the_data_has_the_traps(boda):
    """The traps the questions rely on are really in the data."""
    assert boda.run("SELECT count(*) FROM (SELECT phone FROM riders GROUP BY phone HAVING count(*) > 1) d;"
                    ).check().rows == [("2",)]
    assert boda.run("SELECT count(*) FROM riders r WHERE NOT EXISTS (SELECT 1 FROM trips WHERE rider_id = r.id);"
                    ).check().rows == [("6",)]
    assert boda.run("SELECT count(*) FROM (SELECT 1 FROM trips GROUP BY rider_id, driver_id, requested_at "
                    "HAVING count(*) > 1) d;").check().rows == [("5",)]
