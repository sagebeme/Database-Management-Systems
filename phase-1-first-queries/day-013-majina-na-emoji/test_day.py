"""Day 13: Majina na Emoji."""

import pytest

EMOJI_NAME = "Zawadi \N{SUNFLOWER}"


@pytest.fixture
def guests(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


@pytest.fixture
def converted(guests):
    """The guest list after a correct move to utf8mb4, with the emoji guest added."""
    guests.run("ALTER TABLE guests CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;").check()
    guests.run(f"INSERT INTO guests VALUES (7, '{EMOJI_NAME}', 'bride');").check()
    return guests


def got(db, path, columns):
    result = db.run_file(path).check()
    assert result.columns == columns
    return result.rows


def test_show_charsets(guests, target):
    result = guests.run_file(target / "0-show_charsets.sql").check()
    # information_schema prints its column names in capitals unless you alias them; either is fine.
    assert [c.lower() for c in result.columns] == ["column_name", "character_set_name", "collation_name"]
    rows = result.rows
    assert rows == [("id", "NULL", "NULL"), ("name", "latin1", "latin1_swedish_ci"), ("side", "latin1", "latin1_swedish_ci")]


@pytest.mark.passes_on_starter
def test_latin1_cannot_hold_emoji(guests):
    # Not your work: proof of the problem you're fixing.
    result = guests.run(f"INSERT INTO guests VALUES (7, '{EMOJI_NAME}', 'bride');")
    assert not result.ok and "Incorrect string value" in result.stderr


def test_moves_table_and_database_to_utf8mb4(guests, target):
    guests.run_file(target / "1-move_to_utf8mb4.sql").check()
    table = guests.run(
        "SELECT character_set_name, collation_name FROM information_schema.columns "
        "WHERE table_schema = DATABASE() AND table_name = 'guests' AND column_name = 'name';").check().rows
    assert table == [("utf8mb4", "utf8mb4_unicode_ci")]
    database = guests.run(
        "SELECT default_character_set_name, default_collation_name FROM information_schema.schemata "
        "WHERE schema_name = DATABASE();").check().rows
    assert database == [("utf8mb4", "utf8mb4_unicode_ci")]
    names = guests.run("SELECT name FROM guests ORDER BY id;").check().column(0)
    assert names[2] == "Renée Achieng", "converting must keep the accents"


def test_emoji_guest_after_moving(guests, target):
    guests.run_file(target / "1-move_to_utf8mb4.sql").check()
    guests.run_file(target / "2-add_emoji_guest.sql").check()
    rows = guests.run("SELECT id, name, side FROM guests WHERE id = 7;").check().rows
    assert rows == [("7", EMOJI_NAME, "bride")]


def test_chars_and_bytes(converted, target):
    rows = got(converted, target / "3-chars_and_bytes.sql", ["name", "chars", "bytes"])
    assert rows[2] == ("Renée Achieng", "13", "14"), "é is one character but two bytes in UTF-8"
    assert rows[6] == (EMOJI_NAME, "8", "11"), "the sunflower is one character but four bytes"
    assert rows[0] == ("Amina Hassan", "12", "12")


def test_renee_search(converted, target):
    assert got(converted, target / "4-renee_search.sql", ["name"]) == [("Renée Achieng",), ("Renee Otieno",)]


def test_kata_shouting_names(converted, target):
    assert got(converted, target / "kata.sql", ["name"]) == [("AMINA KARIUKI",)]
