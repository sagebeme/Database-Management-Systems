"""Day 1: Hello, MySQL."""

import pytest

DB = "mama_mboga"


@pytest.fixture
def clean_server(mysql_server):
    """Start and finish every test without a mama_mboga database."""
    mysql_server.run(f"DROP DATABASE IF EXISTS {DB};").check()
    yield mysql_server
    mysql_server.run(f"DROP DATABASE IF EXISTS {DB};").check()


def databases(server) -> list[str]:
    return server.run("SHOW DATABASES;").check().column(0)


def test_lists_every_database(mysql, mysql_server, target):
    # The mysql fixture has just created a database with a random name; your list must show it.
    result = mysql_server.run_file(target / "0-list_databases.sql").check()
    assert result.columns == ["Database"], "SHOW DATABASES prints one column called Database"
    assert "information_schema" in result.column(0)
    assert mysql.database in result.column(0)


def test_creates_the_database(clean_server, target):
    clean_server.run_file(target / "1-create_database_if_missing.sql").check()
    assert DB in databases(clean_server)


def test_creating_twice_is_not_an_error(clean_server, target):
    clean_server.run_file(target / "1-create_database_if_missing.sql").check()
    second = clean_server.run_file(target / "1-create_database_if_missing.sql")
    assert second.ok, f"the second run failed, so IF NOT EXISTS is missing:\n{second.stderr}"
    assert DB in databases(clean_server)


def test_removes_the_database(clean_server, target):
    clean_server.run(f"CREATE DATABASE {DB};").check()
    clean_server.run_file(target / "2-remove_database.sql").check()
    assert DB not in databases(clean_server)


def test_removing_a_missing_database_is_not_an_error(clean_server, target):
    clean_server.run(f"CREATE DATABASE {DB};").check()
    clean_server.run_file(target / "2-remove_database.sql").check()
    second = clean_server.run_file(target / "2-remove_database.sql")
    assert second.ok and DB not in databases(clean_server), \
        f"the second run failed, so IF EXISTS is missing:\n{second.stderr}"


def test_kata_till_maths(mysql_server, target):
    result = mysql_server.run_file(target / "kata.sql").check()
    assert result.columns == ["total"]
    assert result.rows == [("300",)]
