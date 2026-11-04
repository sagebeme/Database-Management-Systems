"""Day 3: Sukuma Prices."""

import pytest

PRODUCE = [
    ("1", "Tomatoes", "kg", "120.00"),
    ("2", "Onions", "kg", "90.00"),
    ("3", "Managu", "bunch", "30.00"),
    ("4", "Avocado", "piece", "15.00"),
]


@pytest.fixture
def shop(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def test_shows_the_create_statement(shop, target):
    result = shop.run_file(target / "0-full_table.sql").check()
    assert result.columns == ["Table", "Create Table"]
    table, create = result.rows[0]
    assert table == "produce"
    assert create.startswith("CREATE TABLE `produce`")
    assert "`price_kes` decimal(7,2)" in create


def test_lists_every_row(shop, target):
    result = shop.run_file(target / "1-list_values.sql").check()
    assert result.columns == ["id", "name", "unit", "price_kes"]
    assert sorted(result.rows) == sorted(PRODUCE)


def test_inserts_sukuma(shop, target):
    shop.run_file(target / "2-insert_value.sql").check()
    rows = shop.run("SELECT * FROM produce ORDER BY id;").check().rows
    assert rows == PRODUCE + [("5", "Sukuma wiki", "bunch", "20.00")]


def test_creates_and_fills_orders(mysql, target):
    mysql.run_file(target / "3-full_creation.sql").check()
    rows = mysql.run("SELECT customer, item, qty FROM orders;").check().rows
    assert sorted(rows) == sorted([
        ("Kamau", "Tomatoes", "2"), ("Njeri", "Managu", "3"),
        ("Otieno", "Avocado", "6"), ("Njeri", "Onions", "1"),
    ])


def test_orders_file_can_be_run_on_an_existing_table(mysql, target):
    mysql.run("CREATE TABLE orders (customer VARCHAR(50), item VARCHAR(50), qty INT);").check()
    mysql.run_file(target / "3-full_creation.sql").check()
    assert mysql.run("SELECT COUNT(*) FROM orders;").check().rows == [("4",)]


def test_lists_two_columns(shop, target):
    result = shop.run_file(target / "4-two_columns.sql").check()
    assert result.columns == ["name", "price_kes"]
    assert sorted(result.rows) == sorted((name, price) for _, name, _, price in PRODUCE)


def test_kata_price_for_three(shop, target):
    result = shop.run_file(target / "kata.sql").check()
    assert result.columns == ["name", "price for 3"]
    assert sorted(result.rows) == sorted([
        ("Tomatoes", "360.00"), ("Onions", "270.00"), ("Managu", "90.00"), ("Avocado", "45.00"),
    ])
