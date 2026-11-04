"""Day 7: Fixing the Register. Each test runs your file, then looks at the whole table."""

import pytest

ORIGINAL = [
    ("1", "Atieno Ouma", "254712000101", "Kakamega", "500.00", "0.00", "active"),
    ("2", "Nafula Wekesa", "254712000102", "Kakamega", "1000.00", "1500.00", "active"),
    ("3", "Akinyi Odera", "254712000103", "Vihiga", "500.00", "0.00", "left"),
    ("4", "Makokha Juma", "25471200010", "Kakamega", "500.00", "2000.00", "active"),
    ("5", "Imali Shikuku", "254712000105", "Vihiga", "750.00", "500.00", "active"),
    ("6", "Auma Were", "254712000106", "Busia", "500.00", "0.00", "left"),
    ("7", "Khaemba Simiyu", "254712000107", "Kakamega", "1000.00", "1200.00", "active"),
    ("8", "Nekesa Barasa", "254712000108", "Bungoma", "500.00", "0.00", "active"),
]


@pytest.fixture
def register(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def table(db):
    return db.run("SELECT * FROM members ORDER BY id;").check().rows


def changed(original, **by_id):
    """The original table with some columns of some rows replaced: changed(ORIGINAL, **{"4": {2: "x"}})."""
    out = []
    for row in original:
        row = list(row)
        for col, value in by_id.get(row[0], {}).items():
            row[col] = value
        out.append(tuple(row))
    return out


def test_fix_phone_changes_only_that_row(register, target):
    register.run_file(target / "0-fix_phone.sql").check()
    assert table(register) == changed(ORIGINAL, **{"4": {2: "254712000104"}})


def test_new_minimum(register, target):
    register.run_file(target / "1-new_minimum.sql").check()
    assert table(register) == changed(ORIGINAL, **{i: {4: "600.00"} for i in ("1", "3", "4", "6", "8")})


def test_kakamega_raise(register, target):
    register.run_file(target / "2-kakamega_raise.sql").check()
    assert table(register) == changed(ORIGINAL, **{
        "1": {4: "550.00"}, "2": {4: "1100.00"}, "4": {4: "550.00"}, "7": {4: "1100.00"},
    })


def test_remove_leavers(register, target):
    register.run_file(target / "3-remove_leavers.sql").check()
    assert table(register) == [r for r in ORIGINAL if r[6] != "left"]


def test_moved(register, target):
    register.run_file(target / "4-moved.sql").check()
    assert table(register) == changed(ORIGINAL, **{"7": {2: "254733000107", 3: "Bungoma"}})


def test_moved_is_one_statement(target):
    text = (target / "4-moved.sql").read_text()
    code = "\n".join(line for line in text.splitlines() if not line.strip().startswith("--"))
    assert code.upper().count("UPDATE") == 1, "change both columns in one UPDATE: SET a = ..., b = ..."


def test_kata_suspensions(register, target):
    register.run_file(target / "kata.sql").check()
    assert table(register) == changed(ORIGINAL, **{
        "2": {6: "suspended"}, "4": {6: "suspended"}, "7": {6: "suspended"},
    })
