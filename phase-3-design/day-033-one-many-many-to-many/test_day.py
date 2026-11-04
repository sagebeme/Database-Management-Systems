"""Day 33: One, Many, Many-to-Many."""

import pytest

from coursekit import er, load_module

MANY = er.MANY


@pytest.fixture
def mapping(target):
    return load_module(target / "mapping.py")


def test_relationships(target):
    d = er.load(target / "relationships.mmd")
    assert len(d.relationships) == 5
    expected = [  # (x, per, how many x per one `per`)
        ("CONSTITUENCY", "COUNTY", (1, MANY)), ("COUNTY", "CONSTITUENCY", (1, 1)),
        ("NATIONAL_ID", "PERSON", (0, 1)), ("PERSON", "NATIONAL_ID", (1, 1)),
        ("UNIT", "STUDENT", (0, MANY)), ("STUDENT", "UNIT", (0, MANY)),
        ("MATATU", "SACCO", (0, MANY)), ("SACCO", "MATATU", (1, 1)),
        ("DOCTOR", "CONSULTING_ROOM", (0, 1)), ("CONSULTING_ROOM", "DOCTOR", (0, 1)),
    ]
    for x, per, card in expected:
        assert d.how_many(x, per=per) == card, f"how many {x} per {per}"


@pytest.mark.parametrize("entities, relationships, multivalued, expected", [
    (["E1", "E2"], [{"a": "E1", "b": "E2", "ratio": "M:N"}], 0, 3),
    (["E1", "E2"], [{"a": "E1", "b": "E2", "ratio": "1:N", "total_b": True}], 0, 2),
    (["E1", "E2"], [{"a": "E1", "b": "E2", "ratio": "1:1", "total_a": True, "total_b": True}], 0, 1),
    (["E1", "E2"], [{"a": "E1", "b": "E2", "ratio": "1:1", "total_a": True}], 0, 2),
    (["E1", "E2"], [{"a": "E1", "b": "E2", "ratio": "1:N"}], 1, 3),
    (["E1", "E2", "E3"], [{"a": "E1", "b": "E2", "ratio": "M:N"}, {"a": "E2", "b": "E3", "ratio": "1:N"},
                          {"a": "E1", "b": "E3", "ratio": "M:N"}], 2, 7),
    (["A"], [], 0, 1),
])
def test_min_tables(mapping, entities, relationships, multivalued, expected):
    assert mapping.min_tables(entities, relationships, multivalued) == expected


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.TABLES_Q1, a.TABLES_Q2, a.TABLES_Q3, a.TABLES_Q4, a.TABLES_Q5] == [3, 2, 1, 3, 4]
    assert a.FOREIGN_KEY_SIDE_1_TO_N == "many"
    assert str(a.ONE_TO_ONE_NEEDS).upper() == "UNIQUE"
    assert a.FK_ENFORCES_EVERY_COUNTY_HAS_A_CONSTITUENCY is False
    assert a.NOT_NULL_ENFORCES_EVERY_CONSTITUENCY_HAS_A_COUNTY is True


def test_national_ids(mysql, day, target):
    mysql.load(day / "setup.sql")
    mysql.run_file(target / "0-national_ids.sql").check()
    mysql.run("INSERT INTO national_ids VALUES ('30000001', 1), ('30000002', 2);").check()
    assert not mysql.run("INSERT INTO national_ids VALUES ('30000003', 1);").ok, "one ID per person"
    assert not mysql.run("INSERT INTO national_ids VALUES ('30000004', 9);").ok, "a real person"
    assert not mysql.run("INSERT INTO national_ids VALUES ('30000005', NULL);").ok, "every ID has a person"


def test_constituencies(mysql, day, target):
    mysql.load(day / "setup.sql")
    mysql.run_file(target / "1-constituencies.sql").check()
    mysql.run("INSERT INTO constituencies (name, county_code) VALUES ('Kisumu Central', '042'), "
              "('Westlands', '047'), ('Langata', '047');").check()
    assert not mysql.run("INSERT INTO constituencies (name, county_code) VALUES ('Nowhere', '099');").ok
    assert not mysql.run("INSERT INTO constituencies (name) VALUES ('Floating');").ok, "exactly one county"


def test_kata_read_the_diagram(mapping, target, tmp_path):
    path = tmp_path / "d.mmd"
    path.write_text("erDiagram\n    CUSTOMER ||--o{ ORDER : places\n    PERSON ||--o| NATIONAL_ID : holds\n"
                    "    ORDER }|--|{ PRODUCT : contains\n")
    assert mapping.describe(path) == [
        "Each CUSTOMER goes with zero or more ORDER.", "Each ORDER goes with exactly one CUSTOMER.",
        "Each PERSON goes with zero or one NATIONAL_ID.", "Each NATIONAL_ID goes with exactly one PERSON.",
        "Each ORDER goes with one or more PRODUCT.", "Each PRODUCT goes with one or more ORDER.",
    ]
