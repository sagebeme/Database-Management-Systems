"""Day 58: Stock Goes Down."""

import pytest

STOCK = "SELECT name, quantity FROM items ORDER BY name;"
START = {"Cooking oil 1L": 12, "Maize flour 2kg": 40, "Milk 500ml": 18, "Rice 1kg": 30, "Sugar 1kg": 25}


@pytest.fixture
def duka(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def stock(db):
    return {name: int(q) for name, q in db.run(STOCK).check().rows}


def order(db, item, number):
    return db.run(f"INSERT INTO orders (item_name, number) VALUES ('{item}', {number});")


def trigger(db, name):
    return db.run("SELECT action_timing, event_manipulation, event_object_table FROM information_schema.triggers "
                  f"WHERE trigger_schema = DATABASE() AND trigger_name = '{name}';").check().rows


def test_decrease_stock(duka, target):
    duka.run_file(target / "0-decrease_stock.sql").check()
    duka.run_file(target / "0-decrease_stock.sql").check()
    assert trigger(duka, "decrease_stock") == [("AFTER", "INSERT", "orders")]
    order(duka, "Sugar 1kg", 3).check()
    order(duka, "Sugar 1kg", 2).check()
    order(duka, "Milk 500ml", 18).check()
    assert stock(duka) == {**START, "Sugar 1kg": 20, "Milk 500ml": 0}


def test_log_stock_change(duka, day, target):
    duka.load(day / "solution" / "0-decrease_stock.sql")
    duka.run_file(target / "1-log_stock_change.sql").check()
    duka.run_file(target / "1-log_stock_change.sql").check()
    order(duka, "Rice 1kg", 4).check()
    duka.run("UPDATE items SET quantity = quantity + 10 WHERE name = 'Cooking oil 1L';").check()
    duka.run("UPDATE items SET quantity = quantity WHERE name = 'Sugar 1kg';").check()
    assert duka.run("SELECT item_name, old_quantity, new_quantity FROM stock_log ORDER BY id;").check().rows == [
        ("Rice 1kg", "30", "26"), ("Cooking oil 1L", "12", "22")], "an update that changes nothing logs nothing"


def test_no_overselling(duka, day, target):
    duka.load(day / "solution" / "0-decrease_stock.sql")
    duka.run_file(target / "2-no_overselling.sql").check()
    duka.run_file(target / "2-no_overselling.sql").check()
    refused = order(duka, "Cooking oil 1L", 13)
    assert not refused.ok and "Not enough stock" in refused.stderr and "45000" in refused.stderr
    assert stock(duka) == START, "a refused order changes nothing"
    assert duka.run("SELECT COUNT(*) FROM orders;").check().rows == [("0",)]
    order(duka, "Cooking oil 1L", 12).check()
    assert stock(duka)["Cooking oil 1L"] == 0, "exactly what's left is fine"
    assert not order(duka, "Cooking oil 1L", 1).ok


def test_cancel_order(duka, day, target):
    duka.load(day / "solution" / "0-decrease_stock.sql")
    duka.run_file(target / "3-cancel_order.sql").check()
    duka.run_file(target / "3-cancel_order.sql").check()
    order(duka, "Maize flour 2kg", 15).check()
    order(duka, "Maize flour 2kg", 5).check()
    duka.run("DELETE FROM orders WHERE number = 15;").check()
    assert stock(duka)["Maize flour 2kg"] == 35


def test_kata_order_changed(duka, day, target):
    duka.load(day / "solution" / "0-decrease_stock.sql")
    duka.load(day / "solution" / "1-log_stock_change.sql")
    duka.run_file(target / "kata.sql").check()
    duka.run_file(target / "kata.sql").check()
    order(duka, "Sugar 1kg", 5).check()
    duka.run("UPDATE orders SET number = 8 WHERE item_name = 'Sugar 1kg';").check()
    assert stock(duka)["Sugar 1kg"] == 17, "three more"
    duka.run("UPDATE orders SET number = 2 WHERE item_name = 'Sugar 1kg';").check()
    assert stock(duka)["Sugar 1kg"] == 23, "six back"
    duka.run("UPDATE orders SET item_name = 'Rice 1kg' WHERE item_name = 'Sugar 1kg';").check()
    assert stock(duka) == {**START, "Rice 1kg": 28}, "sugar fully back, rice down 2"
    duka.run("UPDATE orders SET item_name = 'Milk 500ml', number = 4 WHERE item_name = 'Rice 1kg';").check()
    assert stock(duka) == {**START, "Milk 500ml": 14}
