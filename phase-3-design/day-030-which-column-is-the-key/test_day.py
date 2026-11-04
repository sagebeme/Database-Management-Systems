"""Day 30: Which Column Is the Key?"""

import pytest

from coursekit import load_module

FLEET = [  # invented vehicles
    {"reg_no": "KDA 101A", "chassis_no": "JTF001", "sacco": "Mwangaza", "route": "46", "seats": "14"},
    {"reg_no": "KDB 202B", "chassis_no": "JTF002", "sacco": "Mwangaza", "route": "46", "seats": "33"},
    {"reg_no": "KDC 303C", "chassis_no": "JTF003", "sacco": "Pwani", "route": "111", "seats": "14"},
    {"reg_no": "KDD 404D", "chassis_no": "JTF004", "sacco": "Rift", "route": "111", "seats": "33"},
    {"reg_no": "KDE 505E", "chassis_no": "JTF005", "sacco": "Pwani", "route": "46", "seats": "14"},
]
COLUMNS = ["reg_no", "chassis_no", "sacco", "route", "seats"]


@pytest.fixture
def keys(target):
    return load_module(target / "keys.py")


@pytest.fixture
def answers(target):
    return load_module(target / "answers.py")


def test_unique_on(keys):
    assert keys.unique_on(FLEET, ["reg_no"])
    assert not keys.unique_on(FLEET, ["sacco"])
    assert keys.unique_on(FLEET, ["sacco", "route", "seats"])
    assert not keys.unique_on(FLEET, ["route", "seats"])


def test_could_be_keys(keys):
    assert keys.could_be_keys(FLEET, COLUMNS) == [
        ("reg_no",), ("chassis_no",), ("sacco", "route", "seats"),
    ]


def test_could_be_keys_skips_supersets(keys):
    rows = [{"a": 1, "b": 1, "c": 1}, {"a": 1, "b": 2, "c": 1}, {"a": 2, "b": 1, "c": 2}]
    assert keys.could_be_keys(rows, ["a", "b", "c"]) == [("a", "b"), ("b", "c")]


@pytest.mark.parametrize("attributes, candidate_keys, expected", [
    ("ABCD", ["A"], 8),
    ("ABCD", ["A", "B"], 12),
    ("ABCD", ["A", "BC"], 10),
    ("ABCDE", ["AB", "CD"], 14),
    ("ABCDEF", ["A", "B", "C"], 56),
    ("ABC", ["ABC"], 1),
])
def test_count_superkeys(keys, attributes, candidate_keys, expected):
    assert keys.count_superkeys(list(attributes), [list(k) for k in candidate_keys]) == expected


def test_answers(answers):
    assert answers.SUPERKEYS_OF_R == 10
    assert answers.PRIME_ATTRIBUTES_OF_R == {"A", "B", "C"}
    assert [answers.EVERY_CANDIDATE_KEY_IS_A_SUPERKEY, answers.EVERY_SUPERKEY_IS_A_CANDIDATE_KEY,
            answers.A_PRIMARY_KEY_COLUMN_CAN_BE_NULL, answers.A_FOREIGN_KEY_COLUMN_CAN_BE_NULL,
            answers.A_TABLE_CAN_HAVE_TWO_PRIMARY_KEYS, answers.A_FOREIGN_KEY_MUST_POINT_AT_A_KEY,
            answers.SAMPLE_DATA_CAN_PROVE_A_COLUMN_IS_A_KEY] == [True, False, False, True, False, True, False]


def test_vehicles_table(mysql, day, target):
    mysql.load(day / "setup.sql")
    mysql.run_file(target / "0-vehicles.sql").check()
    mysql.run("INSERT INTO vehicles VALUES ('KDA 101A', 'JTFAAAAAAAAAAA001', 1, 14);").check()
    assert not mysql.run("INSERT INTO vehicles VALUES ('KDA 101A', 'JTFAAAAAAAAAAA002', 1, 14);").ok, "primary key"
    assert not mysql.run("INSERT INTO vehicles VALUES ('KDB 202B', 'JTFAAAAAAAAAAA001', 1, 14);").ok, "alternate key"
    assert not mysql.run("INSERT INTO vehicles VALUES ('KDC 303C', NULL, 1, 14);").ok, "chassis_no required"
    assert not mysql.run("INSERT INTO vehicles VALUES ('KDD 404D', 'JTFAAAAAAAAAAA004', 9, 14);").ok, "a real sacco"
    keys = mysql.run("SELECT constraint_type FROM information_schema.table_constraints "
                     "WHERE table_schema = DATABASE() AND table_name = 'vehicles' ORDER BY 1;").check().column(0)
    assert keys == ["FOREIGN KEY", "PRIMARY KEY", "UNIQUE"]


def test_kata_every_superkey(keys):
    assert keys.all_superkeys(list("ABC"), [["A"]]) == [("A",), ("A", "B"), ("A", "C"), ("A", "B", "C")]
    assert keys.all_superkeys(list("ABCD"), [["A"], ["B", "C"]]) == [
        ("A",), ("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"),
        ("A", "B", "C"), ("A", "B", "D"), ("A", "C", "D"), ("B", "C", "D"), ("A", "B", "C", "D"),
    ]
