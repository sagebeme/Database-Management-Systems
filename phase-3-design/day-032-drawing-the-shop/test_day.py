"""Day 32: Drawing the Shop. The tests read your Mermaid diagrams."""

import pytest

from coursekit import er, load_module

MANY = er.MANY


@pytest.fixture
def shop(target):
    return er.load(target / "shop.mmd")


def test_shop_entities(shop):
    for name in ("CUSTOMER", "CATEGORY", "PRODUCT", "ORDER"):
        assert shop.has_entity(name), f"no {name}"
    assert len(shop.entities) == 4, f"just the four entities, found {sorted(shop.entities)}"


@pytest.mark.parametrize("entity, attributes", [
    ("CUSTOMER", {"id", "name", "phone", "town"}),
    ("CATEGORY", {"id", "name"}),
    ("PRODUCT", {"id", "name", "price", "category_id"}),
    ("ORDER", {"id", "placed_at", "customer_id"}),
])
def test_shop_attributes(shop, entity, attributes):
    assert set(shop.entity(entity)) == attributes
    assert shop.keys(entity) == {"id"}, f"{entity}'s primary key is id"


def test_shop_alternate_and_foreign_keys(shop):
    assert shop.keys("CUSTOMER", "UK") == {"phone"}
    assert shop.keys("CATEGORY", "UK") == {"name"}
    assert shop.keys("PRODUCT", "FK") == {"category_id"}
    assert shop.keys("ORDER", "FK") == {"customer_id"}


def test_shop_relationships(shop):
    assert len(shop.relationships) == 3
    for a, b in [("CUSTOMER", "ORDER"), ("CATEGORY", "PRODUCT"), ("ORDER", "PRODUCT")]:
        found = shop.between(a, b)
        assert len(found) == 1, f"one relationship between {a} and {b}"
        assert found[0].label.strip(), "label every relationship with a verb"
    assert shop.how_many("CUSTOMER", per="ORDER") == (1, 1), "every order has exactly one customer"
    assert shop.how_many("ORDER", per="CUSTOMER")[1] == MANY
    assert shop.how_many("CATEGORY", per="PRODUCT") == (1, 1)
    assert shop.how_many("PRODUCT", per="CATEGORY")[1] == MANY
    assert shop.how_many("PRODUCT", per="ORDER") == (1, MANY), "an order holds at least one product"
    assert shop.how_many("ORDER", per="PRODUCT") == (0, MANY), "a product may never have been ordered"


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.EMAIL, a.FULL_NAME, a.PHONE_NUMBERS, a.AGE, a.DATE_OF_BIRTH, a.HOME_ADDRESS] == [
        "simple", "composite", "multivalued", "derived", "simple", "composite"]
    assert [a.RECTANGLE, a.DOUBLE_RECTANGLE, a.DIAMOND, a.DOUBLE_DIAMOND, a.ELLIPSE, a.UNDERLINED_ELLIPSE,
            a.DOUBLE_ELLIPSE, a.DASHED_ELLIPSE, a.DOUBLE_LINE] == [
        "entity", "weak entity", "relationship", "identifying relationship", "attribute", "key attribute",
        "multivalued attribute", "derived attribute", "total participation"]
    assert [a.STORE_COMPOSITE, a.STORE_MULTIVALUED, a.STORE_DERIVED] == [
        "one column per part", "a table of its own", "not stored, calculated"]


def test_kata_the_stage(target):
    d = er.load(target / "kata.mmd")
    for name in ("SACCO", "MATATU", "DRIVER", "ROUTE"):
        assert d.has_entity(name) and d.keys(name), f"{name}, with a primary key"
    assert d.how_many("SACCO", per="MATATU") == (1, 1) and d.how_many("MATATU", per="SACCO")[1] == MANY
    assert d.how_many("ROUTE", per="MATATU") == (1, 1) and d.how_many("MATATU", per="ROUTE")[1] == MANY
    assert d.how_many("DRIVER", per="MATATU")[1] == MANY and d.how_many("MATATU", per="DRIVER")[1] == MANY
    assert d.keys("MATATU", "FK"), "MATATU points at its sacco and route"
