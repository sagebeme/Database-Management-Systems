"""Day 24: Changing the Shape. Each test loads the original tables, runs one file,
then checks the table's new shape and that no data was lost."""

import pytest


@pytest.fixture
def riverwood(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def columns(db, table):
    """{name: (type, nullable, default)} in column order."""
    rows = db.run(f"""
        SELECT column_name, column_type, is_nullable, IFNULL(column_default, 'none')
        FROM information_schema.columns
        WHERE table_schema = DATABASE() AND table_name = '{table}'
        ORDER BY ordinal_position;""").check().rows
    return {name: tuple(rest) for name, *rest in rows}


def tables(db):
    return db.run("SHOW TABLES;").check().column(0)


def test_add_email(riverwood, target):
    riverwood.run_file(target / "0-add_email.sql").check()
    cols = columns(riverwood, "subscribers")
    assert list(cols) == ["id", "name", "email", "phone", "plan"], "email goes right after name"
    assert cols["email"][:2] == ("varchar(100)", "YES")
    assert riverwood.run("SELECT COUNT(*) FROM subscribers;").check().rows == [("6",)]


def test_plan_required(riverwood, target):
    riverwood.run_file(target / "1-plan_required.sql").check()
    assert columns(riverwood, "subscribers")["plan"] == ("varchar(10)", "NO", "basic")
    plans = riverwood.run("SELECT name, plan FROM subscribers ORDER BY id;").check().rows
    assert plans[2] == ("Chebet Kiprono", "basic") and plans[4] == ("Esther Wanjiru", "basic")
    assert plans[0] == ("Akinyi Odhiambo", "premium"), "don't change plans that were already set"
    assert not riverwood.run("INSERT INTO subscribers (name, plan) VALUES ('X', NULL);").ok
    riverwood.run("INSERT INTO subscribers (name) VALUES ('Gitau Kamau');").check()
    assert riverwood.run("SELECT plan FROM subscribers WHERE name = 'Gitau Kamau';").check().rows == [("basic",)]


def test_rename_phone(riverwood, target):
    riverwood.run_file(target / "2-rename_phone.sql").check()
    cols = columns(riverwood, "subscribers")
    assert "phone" not in cols
    assert list(cols)[2] == "msisdn" and cols["msisdn"][:2] == ("varchar(12)", "YES")
    assert riverwood.run("SELECT msisdn FROM subscribers WHERE id = 1;").check().rows == [("254711000101",)]


def test_clear_session_log(riverwood, target):
    riverwood.run_file(target / "3-clear_session_log.sql").check()
    assert "session_log" in tables(riverwood), "empty the table, don't drop it"
    assert riverwood.run("SELECT COUNT(*) FROM session_log;").check().rows == [("0",)]
    riverwood.run("INSERT INTO session_log (subscriber_id, started_at) VALUES (2, NOW());").check()
    assert riverwood.run("SELECT id FROM session_log;").check().rows == [("1",)], \
        "ids should start again from 1: DELETE keeps counting, TRUNCATE resets"


def test_drop_old_promos(riverwood, target):
    riverwood.run_file(target / "4-drop_old_promos.sql").check()
    assert "old_promo_codes" not in tables(riverwood)
    assert set(tables(riverwood)) == {"session_log", "subscribers"}
    riverwood.run_file(target / "4-drop_old_promos.sql").check()


def test_kata_room_for_long_names(riverwood, target):
    riverwood.run_file(target / "kata.sql").check()
    assert columns(riverwood, "subscribers")["name"][:2] == ("varchar(100)", "NO")
    riverwood.run("INSERT INTO subscribers (name) VALUES ('Nyokabi Wairimu Kamau-Ndung''u wa Mathenge');").check()
    assert not riverwood.run("INSERT INTO subscribers (name) VALUES (NULL);").ok
