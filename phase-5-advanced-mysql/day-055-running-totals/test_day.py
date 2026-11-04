"""Day 55: Running Totals."""

import pytest

# A third till, and Kawangware Fresh opening on Sunday 8 March for once.
SHAKE_UP = """INSERT INTO takings VALUES ('Kawangware Fresh', '2026-03-08', 9100),
    ('Rongai Mart', '2026-03-02', 2000), ('Rongai Mart', '2026-03-03', 1000), ('Rongai Mart', '2026-03-05', 2500),
    ('Rongai Mart', '2026-03-06', 2500), ('Rongai Mart', '2026-03-07', 1700);"""
QUERIES = ["0-running_total", "1-vs_previous", "2-moving_average", "3-big_drops", "kata"]


@pytest.fixture
def tills(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def run(db, folder, name):
    return db.run_file(folder / f"{name}.sql").check().rows


def test_running_total(tills, target):
    rows = run(tills, target, "0-running_total")
    assert rows[:3] == [("Kawangware Fresh", "2026-03-02", "4000", "4000"),
                        ("Kawangware Fresh", "2026-03-03", "4700", "8700"),
                        ("Kawangware Fresh", "2026-03-04", "4400", "13100")]
    assert rows[11] == ("Kawangware Fresh", "2026-03-14", "5700", "67400")
    assert rows[12] == ("Thika Road Duka", "2026-03-02", "5600", "5600"), "each till starts again from zero"
    assert len(rows) == 26


def test_vs_previous(tills, target):
    rows = run(tills, target, "1-vs_previous")
    assert rows[0] == ("Kawangware Fresh", "2026-03-02", "4000", "NULL")
    assert rows[6] == ("Kawangware Fresh", "2026-03-09", "4000", "-4800"), "Monday compares with Saturday"
    assert rows[12][3] == "NULL", "Thika Road Duka's first day has nothing before it"


def test_moving_average(tills, target):
    rows = run(tills, target, "2-moving_average")
    assert [r[3] for r in rows[:6]] == ["4000", "4350", "4367", "5767", "6000", "7467"]


def test_big_drops(tills, target):
    assert run(tills, target, "3-big_drops") == [
        ("Kawangware Fresh", "2026-03-05", "8200", "5400"), ("Kawangware Fresh", "2026-03-07", "8800", "4000"),
        ("Kawangware Fresh", "2026-03-10", "8200", "4600"), ("Thika Road Duka", "2026-03-11", "5600", "3700")]


@pytest.mark.parametrize("name", QUERIES)
def test_on_other_data(tills, day, target, name):
    tills.run(SHAKE_UP).check()
    assert run(tills, target, name) == run(tills, day / "solution", name)


def test_kata_record_days(tills, target):
    assert run(tills, target, "kata") == [
        ("Kawangware Fresh", "2026-03-02", "4000"), ("Kawangware Fresh", "2026-03-03", "4700"),
        ("Kawangware Fresh", "2026-03-05", "8200"), ("Kawangware Fresh", "2026-03-07", "8800"),
        ("Thika Road Duka", "2026-03-02", "5600"), ("Thika Road Duka", "2026-03-14", "5900")]
    tills.run(SHAKE_UP).check()
    rows = run(tills, target, "kata")
    assert ("Kawangware Fresh", "2026-03-08", "9100") in rows
    assert [r for r in rows if r[0] == "Rongai Mart"] == [
        ("Rongai Mart", "2026-03-02", "2000"), ("Rongai Mart", "2026-03-05", "2500")], "equalling the record isn't a record"
