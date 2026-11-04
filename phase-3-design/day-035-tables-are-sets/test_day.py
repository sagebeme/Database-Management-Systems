"""Day 35: Tables Are Sets."""

import pytest

from coursekit import load_module


@pytest.fixture
def rel(target):
    return load_module(target / "relations.py")


def test_make_removes_duplicates(rel):
    r = rel.make(["name", "county"], [("Molo", "Nakuru"), ["Molo", "Nakuru"], ("Thika", "Kiambu")])
    assert r.heading == ("name", "county")
    assert r.rows == frozenset({("Molo", "Nakuru"), ("Thika", "Kiambu")})


def test_make_refuses_bad_shapes(rel):
    with pytest.raises(ValueError):
        rel.make(["name", "name"], [])
    with pytest.raises(ValueError):
        rel.make(["name", "county"], [("Molo",)])


def test_degree_and_cardinality(rel):
    r = rel.make(["name", "county", "code"], [("Molo", "Nakuru", 32), ("Thika", "Kiambu", 22), ("Molo", "Nakuru", 32)])
    assert (rel.degree(r), rel.cardinality(r)) == (3, 2)
    empty = rel.make(["a"], [])
    assert (rel.degree(empty), rel.cardinality(empty)) == (1, 0)


def test_same_ignores_attribute_order(rel):
    r = rel.make(["name", "county"], [("Molo", "Nakuru"), ("Thika", "Kiambu")])
    s = rel.make(["county", "name"], [("Kiambu", "Thika"), ("Nakuru", "Molo")])
    t = rel.make(["county", "name"], [("Nakuru", "Thika"), ("Kiambu", "Molo")])
    assert rel.same(r, s)
    assert not rel.same(r, t)
    assert not rel.same(r, rel.make(["name", "town"], [("Molo", "Nakuru"), ("Thika", "Kiambu")]))


def test_in_domains(rel):
    domains = {"name": {"Molo", "Thika"}, "code": set(range(1, 48))}
    assert rel.in_domains(rel.make(["name", "code"], [("Molo", 32), ("Thika", 22)]), domains)
    assert not rel.in_domains(rel.make(["name", "code"], [("Molo", 32), ("Thika", 99)]), domains)


def test_sql_returns_bags(rel, mysql, day, target):
    mysql.load(day / "setup.sql")
    bag = mysql.run_file(target / "0-counties_as_bag.sql").check()
    as_set = mysql.run_file(target / "1-counties_as_set.sql").check()
    assert bag.columns == ["county"] and len(bag.rows) == 8, "one row per town, duplicates and all"
    assert len(as_set.rows) == 4, "each county once"
    assert rel.same(rel.from_result(bag), rel.from_result(as_set)), "as relations, they're the same"


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.TABLE, a.ROW, a.COLUMN, a.ALLOWED_VALUES_OF_A_COLUMN, a.NUMBER_OF_COLUMNS, a.NUMBER_OF_ROWS,
            a.THE_TABLE_DEFINITION, a.THE_ROWS_RIGHT_NOW] == [
        "relation", "tuple", "attribute", "domain", "degree", "cardinality", "schema", "instance"]
    assert [a.ORDER_OF_TUPLES_MATTERS, a.A_RELATION_CAN_HOLD_THE_SAME_TUPLE_TWICE,
            a.AN_SQL_TABLE_CAN_HOLD_THE_SAME_ROW_TWICE, a.SELECT_WITHOUT_DISTINCT_CAN_RETURN_DUPLICATES] == [
        False, False, True, True]


def test_kata_how_many_relations(rel):
    assert rel.possible_tuples([2, 3]) == 6
    assert rel.possible_relations([2, 3]) == 64
    assert rel.possible_tuples([47, 2]) == 94
    assert rel.possible_relations([1]) == 2, "{} and {(x,)}"
