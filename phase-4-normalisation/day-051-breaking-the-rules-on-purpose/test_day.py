"""Day 51: Breaking the Rules on Purpose."""

import re

import pytest

from coursekit import load_module

TRUTH = "SELECT shop_id, placed_on, COUNT(*), SUM(total) FROM orders GROUP BY shop_id, placed_on ORDER BY 1, 2;"
SUMMARY = "SELECT shop_id, day, order_count, revenue FROM daily_sales ORDER BY 1, 2;"
SHAKE = ("INSERT INTO orders (shop_id, placed_on, total) VALUES (3, '2026-03-02', 999), (1, '2026-03-06', 1),"
         " (4, '2026-03-07', 400);", "DELETE FROM orders WHERE shop_id = 3 AND placed_on = '2026-03-04';")


@pytest.fixture
def dukas(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def test_daily_sales(dukas, target):
    dukas.run_file(target / "0-daily_sales.sql").check()
    rows = dukas.run(SUMMARY).check().rows
    assert len(rows) == 14
    assert ("1", "2026-03-06", "4", "12700") in rows
    assert rows == dukas.run(TRUTH).check().rows
    assert not dukas.run("INSERT INTO daily_sales VALUES (1, '2026-03-06', 1, 1);").ok, "one row per shop and day"


def test_daily_sales_on_other_data(dukas, target):
    for statement in SHAKE:
        dukas.run(statement).check()
    dukas.run_file(target / "0-daily_sales.sql").check()
    assert dukas.run(SUMMARY).check().rows == dukas.run(TRUTH).check().rows


def test_refresh(dukas, day, target):
    dukas.run_file(day / "solution" / "0-daily_sales.sql").check()
    dukas.run_file(target / "1-refresh.sql").check()
    assert dukas.run(SUMMARY).check().rows == dukas.run(TRUTH).check().rows, "running it with nothing new changes nothing"
    for statement in SHAKE:
        dukas.run(statement).check()
    dukas.run_file(target / "1-refresh.sql").check()
    dukas.run_file(target / "1-refresh.sql").check()
    rows = dukas.run(SUMMARY).check().rows
    assert rows == dukas.run(TRUTH).check().rows, "new orders counted, the deleted day gone, nothing doubled"
    assert not [r for r in rows if r[:2] == ("3", "2026-03-04")]


def test_drift(dukas, target):
    assert dukas.run_file(target / "2-drift.sql").check().rows == [
        ("Mama Njeri Groceries", "13", "15"), ("Thika Road Duka", "6", "5")]
    dukas.run("INSERT INTO shops VALUES (5, 'Kitengela Hardware', 2), (6, 'Juja Books', 0);").check()
    dukas.run("UPDATE shops SET orders_count = 8 WHERE id = 2;").check()
    assert dukas.run_file(target / "2-drift.sql").check().rows == [
        ("Kitengela Hardware", "2", "0"), ("Mama Njeri Groceries", "8", "15"), ("Thika Road Duka", "6", "5")], \
        "a shop with no orders is still checked"


def test_fix_drift(dukas, day, target):
    dukas.run("INSERT INTO shops VALUES (5, 'Kitengela Hardware', 2);").check()
    dukas.run_file(target / "3-fix_drift.sql").check()
    assert dukas.run_file(day / "solution" / "2-drift.sql").check().rows == []
    assert dukas.run("SELECT id, orders_count FROM shops ORDER BY id;").check().rows == [
        ("1", "8"), ("2", "15"), ("3", "2"), ("4", "5"), ("5", "0")]


def test_answers(target):
    a = load_module(target / "answers.py")
    assert a.REDUNDANT_COLUMNS == {"shop_name"}
    assert a.TABLES_TO_UPDATE_ON_RENAME == 2
    assert [a.A_SUMMARY_TABLE_CAN_GO_STALE, a.DENORMALISING_MAKES_WRITES_CHEAPER, a.A_MYSQL_VIEW_STORES_ITS_ROWS,
            a.NORMALISE_FIRST_THEN_DENORMALISE_WHAT_A_MEASUREMENT_SAYS_IS_SLOW] == [True, False, False, True]


def test_kata_the_fast_report(dukas, day, target):
    sql = (target / "kata.sql").read_text()
    assert not re.search(r"\b(FROM|JOIN)\s+`?orders`?\b", sql, re.I), "read daily_sales, not orders"
    dukas.run_file(day / "solution" / "0-daily_sales.sql").check()
    assert dukas.run_file(target / "kata.sql").check().rows == [
        ("Kawangware Fresh", "2026-03-06", "12700"), ("Mama Njeri Groceries", "2026-03-06", "10650"),
        ("Ongata Rongai Mart", "2026-03-04", "6500"), ("Thika Road Duka", "2026-03-05", "3850")]
    dukas.run("INSERT INTO daily_sales VALUES (3, '2026-03-02', 1, 6500);").check()
    dukas.run("UPDATE daily_sales SET revenue = 9999 WHERE shop_id = 4 AND day = '2026-03-02';").check()
    assert dukas.run_file(target / "kata.sql").check().rows == [
        ("Kawangware Fresh", "2026-03-06", "12700"), ("Mama Njeri Groceries", "2026-03-06", "10650"),
        ("Ongata Rongai Mart", "2026-03-02", "6500"), ("Thika Road Duka", "2026-03-02", "9999")], \
        "a tie goes to the earlier day"
