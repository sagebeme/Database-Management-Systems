"""Day 9: Sales by Category."""

import pytest


@pytest.fixture
def duka(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def same(db, path, reference):
    got = db.run_file(path).check()
    want = db.run(reference).check()
    assert got.columns == want.columns
    assert got.rows == want.rows
    return got


def test_sales_per_category(duka, target):
    got = same(duka, target / "0-sales_per_category.sql",
               "SELECT category, COUNT(*) AS sales FROM sales GROUP BY category ORDER BY sales DESC, category;")
    assert got.rows[0] == ("Food", "19")


def test_revenue_per_category(duka, target):
    got = same(duka, target / "1-revenue_per_category.sql",
               "SELECT category, SUM(qty * unit_price) AS revenue FROM sales GROUP BY category ORDER BY revenue DESC;")
    assert got.rows == [("Food", "8175.00"), ("Household", "980.00"), ("Airtime", "700.00"), ("Stationery", "340.00")]


def test_daily_takings(duka, target):
    got = same(duka, target / "2-daily_takings.sql",
               "SELECT sold_on, SUM(qty * unit_price) AS takings FROM sales GROUP BY sold_on ORDER BY sold_on;")
    assert len(got.rows) == 12


def test_payment_split(duka, target):
    same(duka, target / "3-payment_split.sql",
         "SELECT payment, COUNT(*) AS sales, SUM(qty * unit_price) AS revenue FROM sales GROUP BY payment ORDER BY payment;")


def test_best_sellers(duka, target):
    got = same(duka, target / "4-best_sellers.sql",
               "SELECT item, SUM(qty) AS units FROM sales GROUP BY item ORDER BY units DESC, item LIMIT 3;")
    assert len(got.rows) == 3


def test_kata_busiest_day(duka, target):
    got = duka.run_file(target / "kata.sql").check()
    assert got.columns == ["sold_on", "takings"]
    assert got.rows == [("2025-06-11", "2260.00")]
