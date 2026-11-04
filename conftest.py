"""Fixtures every day's tests share.

    target   the folder being tested: the day's starter/ (yours), or solution/ when
             DBMS_TARGET=solution (that's how tools/verify.py proves the answers work)
    mysql    a brand-new, empty MySQL database for one test, dropped afterwards
    postgres the same, in PostgreSQL
    mongo    the same, in MongoDB
    redis_db a Redis client on an empty database, flushed afterwards

If a server isn't running, tests that need it are skipped with a hint, unless DBMS_REQUIRE=1
(CI sets it), which turns that into a failure so nothing passes by being skipped.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent / "tools"))

from coursekit import (  # noqa: E402
    DatabaseUnavailable, Mongo, MySQL, Postgres, new_name, setting,
)

HINT = "Start it with: tools/devdb.sh up  (or see 'Setting up' in the README)"


def _unavailable(what: str, error: Exception) -> None:
    message = f"{what} isn't available ({error}). {HINT}"
    if os.environ.get("DBMS_REQUIRE") == "1":
        pytest.fail(message)
    pytest.skip(message)


@pytest.fixture
def day(request) -> Path:
    """The day's folder, e.g. phase-1-first-queries/day-001-hello-mysql."""
    return Path(request.path).parent


@pytest.fixture
def target(day: Path) -> Path:
    which = os.environ.get("DBMS_TARGET", "starter")
    if which not in ("starter", "solution"):
        raise pytest.UsageError("DBMS_TARGET must be 'starter' or 'solution'")
    return day / which


class MySQLDatabase(MySQL):
    """A MySQL database that exists only for one test."""

    def load(self, path: Path | str) -> None:
        """Run a setup file (tables and rows the task starts from); fail loudly if it breaks."""
        self.run_file(path).check()


@pytest.fixture
def mysql():
    server = MySQL()
    try:
        server.ping()
    except DatabaseUnavailable as e:
        _unavailable("MySQL", e)
    name = new_name()
    server.run(f"CREATE DATABASE `{name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;", database=None).check()
    db = MySQLDatabase(name)
    try:
        yield db
    finally:
        server.run(f"DROP DATABASE IF EXISTS `{name}`;", database=None)


@pytest.fixture
def mysql_server():
    """No database selected: for tasks that list, create or drop databases themselves."""
    server = MySQLDatabase(None)
    try:
        server.ping()
    except DatabaseUnavailable as e:
        _unavailable("MySQL", e)
    return server


class PostgresDatabase(Postgres):
    def load(self, path: Path | str) -> None:
        self.run_file(path).check()


@pytest.fixture
def postgres():
    server = Postgres()
    try:
        server.ping()
    except DatabaseUnavailable as e:
        _unavailable("PostgreSQL", e)
    name = new_name()
    server.run(f'CREATE DATABASE "{name}" ENCODING \'UTF8\' TEMPLATE template0;').check()
    try:
        yield PostgresDatabase(name)
    finally:
        server.run(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE);')


@pytest.fixture
def mongo():
    name = new_name()
    db = Mongo(name)
    try:
        result = db.run("db.runCommand({ping: 1}).ok")
    except DatabaseUnavailable as e:
        _unavailable("MongoDB", e)
    if not result.ok:
        _unavailable("MongoDB", RuntimeError(result.stderr.strip() or result.stdout.strip()))
    try:
        yield db
    finally:
        db.run("db.dropDatabase()")


@pytest.fixture
def mongo_url() -> str:
    return setting("MONGO_URL")


@pytest.fixture
def redis_db():
    try:
        import redis
    except ImportError as e:  # pragma: no cover
        _unavailable("The redis package", e)
    client = redis.Redis.from_url(setting("REDIS_URL"))
    try:
        client.ping()
    except Exception as e:  # noqa: BLE001 - any connection problem means "not running"
        _unavailable("Redis", e)
    client.flushdb()
    try:
        yield client
    finally:
        client.flushdb()


# tools/verify.py sets DBMS_REPORT to a file path and reads every test's outcome from it.
_report_path = os.environ.get("DBMS_REPORT")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    if not _report_path:
        return
    report = outcome.get_result()
    if report.when == "call" or (report.when == "setup" and report.outcome != "passed"):
        import json
        with open(_report_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "nodeid": item.nodeid,
                "outcome": report.outcome,
                "passes_on_starter": item.get_closest_marker("passes_on_starter") is not None,
            }) + "\n")
