"""Day 67: Isolation Levels.

Your experiments run against real MySQL and PostgreSQL servers at every level, and what they find is compared
with how each engine really behaves.
"""

import pytest

from coursekit import load_module

LEVELS = ["READ UNCOMMITTED", "READ COMMITTED", "REPEATABLE READ", "SERIALIZABLE"]
# (sees a dirty read, reads repeat, sees a phantom), for each engine and level.
FOUND = {
    "mysql": {"READ UNCOMMITTED": (True, False, True), "READ COMMITTED": (False, False, True),
              "REPEATABLE READ": (False, True, False), "SERIALIZABLE": (False, True, False)},
    "postgres": {"READ UNCOMMITTED": (False, False, True), "READ COMMITTED": (False, False, True),
                 "REPEATABLE READ": (False, True, False), "SERIALIZABLE": (False, True, False)},
}


@pytest.fixture(params=["mysql", "postgres"])
def engine(request, day):
    db = request.getfixturevalue(request.param)
    db.load(day / "setup.sql")
    return request.param, db


@pytest.mark.parametrize("level", LEVELS)
def test_experiments(engine, target, level):
    name, db = engine
    levels = load_module(target / "levels.py")
    found = (levels.sees_uncommitted(db.connect, name, level), levels.repeatable(db.connect, name, level),
             levels.sees_phantom(db.connect, name, level))
    assert found == FOUND[name][level], "(dirty read seen, reads repeat, phantom seen)"


def test_experiments_leave_nothing_open(engine, target):
    name, db = engine
    levels = load_module(target / "levels.py")
    levels.sees_uncommitted(db.connect, name, "READ COMMITTED")
    assert db.run("SELECT balance FROM accounts;").check().rows == [("1500",)], "A's change was rolled back"
    levels.repeatable(db.connect, name, "READ COMMITTED")
    assert db.run("SELECT balance FROM accounts;").check().rows == [("1600",)], "A's +100 was committed"
    levels.sees_phantom(db.connect, name, "READ COMMITTED")
    assert db.run("SELECT COUNT(*) FROM bookings WHERE trip_id = 2;").check().rows == [("3",)]


def test_answers(target):
    a = load_module(target / "answers.py")
    assert a.STANDARD_ALLOWS == {
        "READ UNCOMMITTED": {"dirty read", "non-repeatable read", "phantom"},
        "READ COMMITTED": {"non-repeatable read", "phantom"}, "REPEATABLE READ": {"phantom"}, "SERIALIZABLE": set()}
    assert (a.MYSQL_DEFAULT, a.POSTGRES_DEFAULT) == ("REPEATABLE READ", "READ COMMITTED")
    assert [a.POSTGRES_EVER_SHOWS_A_DIRTY_READ, a.MYSQL_REPEATABLE_READ_SHOWS_PHANTOMS_TO_A_PLAIN_SELECT,
            a.MYSQL_SERIALIZABLE_MAKES_WRITERS_WAIT_FOR_READERS] == [False, False, True]


@pytest.mark.parametrize("level, on_call", [("READ COMMITTED", 0), ("REPEATABLE READ", 0), ("SERIALIZABLE", 1)])
def test_kata_write_skew(engine, target, level, on_call):
    name, db = engine
    kata = load_module(target / "kata.py")
    assert kata.write_skew(db.connect, name, level) == on_call
