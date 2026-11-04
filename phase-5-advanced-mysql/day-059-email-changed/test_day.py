"""Day 59: Email Changed."""

import pytest


@pytest.fixture
def pamoja(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def user(db, name):
    return db.run(f"SELECT email, valid_email FROM users WHERE name = '{name}';").check().rows[0]


def set_email(db, name, email):
    return db.run(f"UPDATE users SET email = '{email}' WHERE name = '{name}';")


def test_reset_valid_email(pamoja, target):
    pamoja.run_file(target / "0-reset_valid_email.sql").check()
    pamoja.run_file(target / "0-reset_valid_email.sql").check()
    set_email(pamoja, "Wanjiku", "wanjiku.kamau@pamoja.test").check()
    assert user(pamoja, "Wanjiku") == ("wanjiku.kamau@pamoja.test", "0")
    pamoja.run("UPDATE users SET name = 'Chebet Rono' WHERE name = 'Chebet';").check()
    assert user(pamoja, "Chebet Rono") == ("chebet@pamoja.test", "1"), "a name change keeps the email confirmed"
    set_email(pamoja, "Akinyi", "akinyi@pamoja.test").check()
    assert user(pamoja, "Akinyi") == ("akinyi@pamoja.test", "1"), "the same address isn't a change"
    pamoja.run("UPDATE users SET valid_email = 1 WHERE name = 'Otieno';").check()
    assert user(pamoja, "Otieno") == ("otieno@pamoja.test", "1"), "confirming still works"


def test_clean_email(pamoja, day, target):
    pamoja.load(day / "solution" / "0-reset_valid_email.sql")
    pamoja.run_file(target / "1-clean_email.sql").check()
    pamoja.run_file(target / "1-clean_email.sql").check()
    pamoja.run("INSERT INTO users (email, name) VALUES ('  Halima@Pamoja.TEST ', 'Halima');").check()
    assert user(pamoja, "Halima") == ("halima@pamoja.test", "0")
    set_email(pamoja, "Wanjiku", " wanjiku@pamoja.test  ").check()
    assert user(pamoja, "Wanjiku") == ("wanjiku@pamoja.test", "1"), \
        "cleaned before reset_valid_email looks at it, so it isn't a new address"
    set_email(pamoja, "Chebet", " CHEBET.R@pamoja.test").check()
    assert user(pamoja, "Chebet") == ("chebet.r@pamoja.test", "0")
    order = pamoja.run("SELECT trigger_name FROM information_schema.triggers WHERE trigger_schema = DATABASE() "
                       "AND event_manipulation = 'UPDATE' AND event_object_table = 'users' "
                       "ORDER BY action_order;").check().rows
    assert order == [("clean_email_update",), ("reset_valid_email",)]


def test_email_history(pamoja, day, target):
    pamoja.load(day / "solution" / "0-reset_valid_email.sql")
    pamoja.run_file(target / "2-email_history.sql").check()
    pamoja.run_file(target / "2-email_history.sql").check()
    set_email(pamoja, "Otieno", "ouma@pamoja.test").check()
    set_email(pamoja, "Otieno", "otieno.ouma@pamoja.test").check()
    pamoja.run("UPDATE users SET name = 'Mutua M' WHERE name = 'Mutua';").check()
    set_email(pamoja, "Akinyi", "akinyi@pamoja.test").check()
    assert pamoja.run("SELECT user_id, old_email, new_email FROM email_history ORDER BY id;").check().rows == [
        ("2", "otieno@pamoja.test", "ouma@pamoja.test"), ("2", "ouma@pamoja.test", "otieno.ouma@pamoja.test")]


def test_keep_verified_users(pamoja, target):
    pamoja.run_file(target / "3-keep_verified_users.sql").check()
    pamoja.run_file(target / "3-keep_verified_users.sql").check()
    pamoja.run("DELETE FROM users WHERE name = 'Otieno';").check()
    refused = pamoja.run("DELETE FROM users WHERE name = 'Wanjiku';")
    assert not refused.ok and "Verified users cannot be deleted" in refused.stderr
    assert not pamoja.run("DELETE FROM users;").ok, "one verified user stops the whole statement"
    assert pamoja.run("SELECT name FROM users ORDER BY id;").check().rows == [
        ("Wanjiku",), ("Chebet",), ("Mutua",), ("Akinyi",)]


def test_kata_limit_email_changes(pamoja, day, target):
    for name in ("0-reset_valid_email", "1-clean_email", "2-email_history"):
        pamoja.load(day / "solution" / f"{name}.sql")
    pamoja.run_file(target / "kata.sql").check()
    pamoja.run_file(target / "kata.sql").check()
    for n in range(1, 4):
        set_email(pamoja, "Mutua", f"mutua{n}@pamoja.test").check()
    refused = set_email(pamoja, "Mutua", "mutua4@pamoja.test")
    assert not refused.ok and "Too many email changes" in refused.stderr
    assert user(pamoja, "Mutua") == ("mutua3@pamoja.test", "0")
    pamoja.run("UPDATE users SET valid_email = 1 WHERE name = 'Mutua';").check()
    set_email(pamoja, "Mutua", "MUTUA3@pamoja.test ").check()
    set_email(pamoja, "Otieno", "otieno2@pamoja.test").check()
