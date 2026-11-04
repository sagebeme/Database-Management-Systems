"""Day 48: First and Second Normal Form."""

import pytest

from coursekit import load_module
from coursekit.fds import attrs, parse

ENROL = attrs("student course name fee grade")
ENROL_FDS = parse("student -> name; course -> fee; student course -> grade")


@pytest.fixture
def nf(target):
    return load_module(target / "second_nf.py")


@pytest.fixture
def chama(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def test_member_phones(chama, target):
    chama.run_file(target / "0-member_phones.sql").check()
    rows = chama.run("SELECT member_id, phone FROM member_phones ORDER BY 1, 2;").check().rows
    assert rows == [("1", "254711000001"), ("1", "254722000001"), ("2", "254733000002"), ("3", "254711000003"),
                    ("3", "254744000003"), ("3", "254755000003"), ("5", "254766000005")]
    assert not chama.run("INSERT INTO member_phones VALUES (1, '254711000001');").ok, "each phone once per member"
    assert not chama.run("INSERT INTO member_phones VALUES (9, '254700000000');").ok, "a real member"


def test_member_phones_on_other_data(mysql, day, target):
    mysql.load(day / "setup.sql")
    mysql.run("INSERT INTO members_raw VALUES (6, 'Kamau', ' 254777000006 ,254788000006');").check()
    mysql.run_file(target / "0-member_phones.sql").check()
    assert mysql.run("SELECT phone FROM member_phones WHERE member_id = 6 ORDER BY 1;").check().rows == [
        ("254777000006",), ("254788000006",)]


@pytest.mark.parametrize("name, want", [
    ("1-phones_per_member", [("Chebet", "3"), ("Wanjiku", "2"), ("Akinyi", "1"), ("Otieno", "1"), ("Mutua", "0")]),
    ("2-who_owns_this", [("Chebet",)]),
])
def test_queries(chama, day, target, name, want):
    chama.run_file(day / "solution" / "0-member_phones.sql").check()
    assert chama.run_file(target / f"{name}.sql").check().rows == want


def test_non_prime(nf):
    assert nf.non_prime(ENROL, ENROL_FDS) == attrs("name fee grade")


def test_partial_dependencies(nf):
    assert nf.partial_dependencies(ENROL, ENROL_FDS) == [
        (attrs("course"), "fee"), (attrs("student"), "name")]
    assert nf.partial_dependencies(attrs("ABCD"), parse("AB->C; B->D")) == [(attrs("B"), "D")]
    assert nf.partial_dependencies(attrs("ABC"), parse("A->B; B->C")) == [], "a single-attribute key can't be split"
    assert nf.partial_dependencies(attrs("ABC"), parse("AB->C; C->B")) == [], "B is prime, so C -> B isn't partial"


@pytest.mark.parametrize("schema, fds, ok", [
    ("student course name fee grade", "student -> name; course -> fee; student course -> grade", False),
    ("ABC", "A->B; B->C", True),
    ("ABCD", "AB->CD; A->C", False),
    ("ABCD", "AB->CD; C->D", True),
    ("ABC", "AB->C; C->B", True),
])
def test_is_2nf(nf, schema, fds, ok):
    assert nf.is_2nf(attrs(schema), parse(fds)) is ok


def test_answers(target):
    a = load_module(target / "answers.py")
    assert a.CANDIDATE_KEY == {"student", "course"}
    assert a.NON_PRIME_ATTRIBUTES == {"name", "fee", "grade"}
    assert a.IS_R_IN_2NF is False
    assert [a.A_TABLE_WITH_A_COMMA_SEPARATED_LIST_COLUMN_IS_IN_1NF,
            a.A_RELATION_WHOSE_KEYS_ARE_ALL_SINGLE_ATTRIBUTES_IS_IN_2NF,
            a.TWO_NF_RESTRICTS_PRIME_ATTRIBUTES_TOO, a.A_PARTIAL_DEPENDENCY_NEEDS_A_COMPOSITE_KEY] == [False, True, False, True]


def test_kata_pull_them_out(nf):
    assert nf.to_2nf(ENROL, ENROL_FDS) == [attrs("course fee"), attrs("student name"), attrs("student course grade")]
    assert nf.to_2nf(attrs("ABCD"), parse("AB->C; B->D")) == [attrs("BD"), attrs("ABC")]
    assert nf.to_2nf(attrs("ABC"), parse("A->B; B->C")) == [attrs("ABC")]
