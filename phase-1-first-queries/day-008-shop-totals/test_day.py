"""Day 8: Shop Totals."""

import pytest


@pytest.fixture
def duka(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def answer(db, path):
    result = db.run_file(path).check()
    assert len(result.rows) == 1, "an aggregate without GROUP BY gives exactly one row"
    return result.columns, result.rows[0]


def test_count(duka, target):
    assert answer(duka, target / "0-count_sales.sql") == (["sales"], ("40",))


def test_count_follows_the_data(duka, target):
    duka.run("DELETE FROM sales WHERE id > 30;").check()
    assert answer(duka, target / "0-count_sales.sql") == (["sales"], ("30",))


def test_revenue(duka, target):
    assert answer(duka, target / "1-revenue.sql") == (["revenue"], ("10195.00",))


def test_average_price(duka, target):
    assert answer(duka, target / "2-average_price.sql") == (["average_price"], ("130.50",))


def test_cheapest_and_dearest(duka, target):
    assert answer(duka, target / "3-cheapest_dearest.sql") == (["cheapest", "dearest"], ("5.00", "340.00"))


def test_mpesa_takings(duka, target):
    want = duka.run("SELECT COUNT(*), SUM(qty * unit_price) FROM sales WHERE payment = 'mpesa';").check().rows[0]
    assert answer(duka, target / "4-mpesa_takings.sql") == (["mpesa_sales", "mpesa_revenue"], want)


def test_kata_items(duka, target):
    assert answer(duka, target / "kata.sql") == (["items"], ("11",))
