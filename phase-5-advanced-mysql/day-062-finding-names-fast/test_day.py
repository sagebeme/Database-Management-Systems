"""Day 62: Finding Names Fast.

EXPLAIN's choices depend on the optimizer's estimates, so these tests only ask about queries where an index is
the clear winner on this data.
"""

import pytest

REPORT = "SELECT customer_id, SUM(total) FROM orders WHERE placed_on >= '2026-01-01' GROUP BY customer_id"


@pytest.fixture
def fast(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def index_columns(db, table, index):
    return db.run("SELECT column_name, sub_part FROM information_schema.statistics WHERE table_schema = DATABASE() "
                  f"AND table_name = '{table}' AND index_name = '{index}' ORDER BY seq_in_index;").check().rows


def explain(db, query):
    result = db.run(f"EXPLAIN {query};").check()
    row = dict(zip(result.columns, result.rows[0]))
    return row["key"], row["type"], row["Extra"]


def test_index_my_names(fast, target):
    fast.run_file(target / "0-index_my_names.sql").check()
    assert index_columns(fast, "names", "idx_name_first") == [("name", "1")]
    assert explain(fast, "SELECT COUNT(*) FROM names WHERE name LIKE 'Z%'")[0] == "idx_name_first"
    assert fast.run("SELECT COUNT(*) FROM names WHERE name LIKE 'Z%';").check().rows == [("2500",)]


def test_index_name_score(fast, target):
    fast.run_file(target / "1-index_name_score.sql").check()
    assert index_columns(fast, "names", "idx_name_first_score") == [("name", "1"), ("score", "NULL")]
    assert explain(fast, "SELECT name, score FROM names WHERE name LIKE 'Z%' AND score < 80")[0] == "idx_name_first_score"


def test_index_customer(fast, target):
    fast.run_file(target / "2-index_customer.sql").check()
    assert index_columns(fast, "orders", "idx_orders_customer") == [("customer_id", "NULL")]
    key, kind, _ = explain(fast, "SELECT * FROM orders WHERE customer_id = 42")
    assert (key, kind) == ("idx_orders_customer", "ref"), "straight to customer 42's rows"


def test_june_sales(fast, target):
    result = fast.run_file(target / "3-june_sales.sql").check()
    assert index_columns(fast, "orders", "idx_placed_on") == [("placed_on", "NULL")]
    want = fast.run("SELECT COUNT(*), SUM(total) FROM orders "
                    "WHERE YEAR(placed_on) = 2025 AND MONTH(placed_on) = 6;").check().rows
    assert result.rows == want
    statements = [s.strip() for s in (target / "3-june_sales.sql").read_text().split("this line.")[-1].split(";")]
    query = [s for s in statements if s.upper().startswith("SELECT")][-1]
    key, kind, _ = explain(fast, query)
    assert (key, kind) == ("idx_placed_on", "range"), \
        "the index isn't used: don't wrap placed_on in a function; compare it with a range of dates"


def test_kata_covering_index(fast, target):
    fast.run_file(target / "kata.sql").check()
    key, _, extra = explain(fast, REPORT)
    assert key == "idx_customer_report"
    assert "Using index" in extra.split("; "), "every column the query needs must be in the index"
