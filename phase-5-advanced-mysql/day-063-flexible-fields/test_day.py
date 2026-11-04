"""Day 63: Flexible Fields."""

import pytest

INSERT = "INSERT INTO products (id, name, category, price, attributes) VALUES ({}, '{}', '{}', {}, '{}');"
SHAKE_UP = [
    INSERT.format(11, "Simu Poa Max", "phone", 54999, '{"ram_gb": 12, "storage_gb": 512, "tags": ["new", "premium"]}'),
    INSERT.format(12, "Mandazi pack", "food", 100, '{"weight_g": 300, "tags": ["fresh"]}'),
    INSERT.format(13, "Gumboots", "shoes", 900, '{"size": 44, "tags": []}'),
]
QUERIES = ["0-phones", "3-new_arrivals", "4-tag_counts"]


@pytest.fixture
def catalogue(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def run(db, folder, name):
    return db.run_file(folder / f"{name}.sql").check().rows


def test_phones(catalogue, target):
    assert run(catalogue, target, "0-phones") == [
        ("Simu Poa A3", "4", "128", "11999"), ("Simu Poa A5", "4", "64", "15999"), ("Simu Poa X", "8", "256", "32999")]


def test_on_offer(catalogue, target):
    before = dict(catalogue.run("SELECT id, attributes FROM products WHERE price >= 500;").check().rows)
    catalogue.run_file(target / "1-on_offer.sql").check()
    assert catalogue.run("SELECT id, attributes->'$.on_offer', attributes->>'$.weight_g' FROM products "
                         "WHERE JSON_CONTAINS_PATH(attributes, 'one', '$.on_offer') ORDER BY id;").check().rows == [
        ("8", "true", "2000"), ("9", "true", "250")], "a JSON true, and the other details kept"
    assert dict(catalogue.run("SELECT id, attributes FROM products WHERE price >= 500;").check().rows) == before


def test_ram_column(catalogue, target):
    catalogue.run_file(target / "2-ram_column.sql").check()
    column = catalogue.run("SELECT data_type, extra FROM information_schema.columns WHERE table_schema = DATABASE() "
                           "AND table_name = 'products' AND column_name = 'ram_gb';").check().rows
    assert len(column) == 1 and column[0][0] == "int" and "GENERATED" in column[0][1]
    assert catalogue.run("SELECT column_name FROM information_schema.statistics WHERE table_schema = DATABASE() "
                         "AND index_name = 'idx_ram_gb';").check().rows == [("ram_gb",)]
    assert catalogue.run("SELECT id, ram_gb FROM products WHERE id IN (1, 3, 9) ORDER BY id;").check().rows == [
        ("1", "3"), ("3", "8"), ("9", "NULL")]
    catalogue.run("UPDATE products SET attributes = JSON_SET(attributes, '$.ram_gb', 6) WHERE id = 1;").check()
    assert catalogue.run("SELECT ram_gb FROM products WHERE id = 1;").check().rows == [("6",)], "it follows the JSON"
    assert not catalogue.run("UPDATE products SET ram_gb = 99 WHERE id = 1;").ok, "you can't write to it"


def test_new_arrivals(catalogue, target):
    assert run(catalogue, target, "3-new_arrivals") == [
        ("Maasai sandals", "shoes"), ("Simu Poa A5", "phone"), ("Simu Poa X", "phone"), ("Solar lamp", "electronics")]


def test_tag_counts(catalogue, target):
    assert run(catalogue, target, "4-tag_counts") == [
        ("new", "4"), ("handmade", "2"), ("staple", "2"), ("budget", "1"), ("fresh", "1"), ("premium", "1")]


@pytest.mark.parametrize("name", QUERIES)
def test_on_other_data(catalogue, day, target, name):
    for statement in SHAKE_UP:
        catalogue.run(statement).check()
    assert run(catalogue, target, name) == run(catalogue, day / "solution", name)


def test_kata_phone_shape(catalogue, target):
    catalogue.run_file(target / "kata.sql").check()
    phone = lambda i, attrs: catalogue.run(INSERT.format(i, f"Phone {i}", "phone", 1000, attrs))
    assert not phone(20, '{"ram_gb": "4", "storage_gb": 64}').ok, "a number, not text"
    assert not phone(21, '{"ram_gb": 4}').ok, "storage_gb is required"
    assert not phone(22, '{"storage_gb": 4}').ok, "ram_gb is required"
    assert not phone(23, '{"ram_gb": -1, "storage_gb": 16}').ok, "not negative"
    assert not phone(24, '{"ram_gb": 1.5, "storage_gb": 16}').ok, "whole numbers"
    phone(25, '{"ram_gb": 2, "storage_gb": 16, "tags": ["budget"]}').check()
    catalogue.run(INSERT.format(26, "Lamp", "electronics", 500, '{"watts": "five"}')).check()
    assert not catalogue.run("UPDATE products SET attributes = JSON_REMOVE(attributes, '$.ram_gb') WHERE id = 1;").ok
