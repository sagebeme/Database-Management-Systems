"""Day 15: One Table Is Not Enough."""

import pytest


@pytest.fixture
def shop(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def got(db, path, columns):
    result = db.run_file(path).check()
    assert result.columns == columns
    return result.rows


def test_many_phones(shop, target):
    assert got(shop, target / "0-many_phones.sql", ["customer_name", "phones"]) == [("Kamau Njoroge", "2")]


def test_fix_kamau(shop, target):
    shop.run_file(target / "1-fix_kamau.sql").check()
    phones = shop.run("SELECT DISTINCT customer_phone FROM orders_flat WHERE customer_name = 'Kamau Njoroge';").check().rows
    assert phones == [("254720000001",)]
    others = shop.run("SELECT COUNT(*) FROM orders_flat WHERE customer_phone = '254720000001';").check().rows
    assert others == [("4",)], "only Kamau's four rows should have his number"


def test_customers_table(shop, target):
    shop.run("UPDATE orders_flat SET customer_phone = '254720000001' WHERE customer_name = 'Kamau Njoroge';").check()
    shop.run_file(target / "2-customers_table.sql").check()
    rows = shop.run("SELECT name, phone, town FROM customers ORDER BY name;").check().rows
    assert rows == [
        ("Akinyi Otieno", "254720000002", "Naivasha"),
        ("Chebet Kirui", "254720000003", "Molo"),
        ("Kamau Njoroge", "254720000001", "Nakuru"),
    ]


def test_price_conflicts(shop, target):
    assert got(shop, target / "3-price_conflicts.sql", ["item", "prices"]) == [("Exercise book", "2")]


def test_items_table(shop, target):
    shop.run_file(target / "4-items_table.sql").check()
    rows = shop.run("SELECT name, price FROM items ORDER BY name;").check().rows
    assert rows == [
        ("Biro pen", "20.00"), ("Exercise book", "65.00"), ("Geometry set", "350.00"),
        ("Manila paper", "15.00"), ("Ruler", "40.00"),
    ]


def test_kata_lost_with_the_order(shop, target):
    assert got(shop, target / "kata.sql", ["item", "order_id"]) == [
        ("Geometry set", "5"), ("Manila paper", "7"), ("Ruler", "3"),
    ]
