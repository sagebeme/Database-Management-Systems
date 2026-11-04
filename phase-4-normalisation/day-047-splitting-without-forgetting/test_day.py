"""Day 47: Splitting Without Forgetting."""

import pytest

from coursekit import load_module
from coursekit.fds import attrs, fmt, parse

ZONES = """INSERT INTO zones VALUES ('N01', 'Nakuru'), ('N02', 'Nakuru'), ('E01', 'Eldoret');
INSERT INTO addresses VALUES ('Kenyatta Avenue', 'N01'), ('Oginga Odinga Road', 'E01'), ('Moi Road', 'N02');"""


@pytest.fixture
def dp(target):
    return load_module(target / "preserve.py")


def parts(*names):
    return [attrs(n) for n in names]


def test_preserved(dp):
    f = parse("A->B; B->C; C->D; D->A")
    assert all(dp.preserved(fd, parts("AB", "BC", "CD"), f) for fd in f), "D->A survives through the others"
    g = parse("AB->C; C->A")
    assert not dp.preserved(g[0], parts("AC", "BC"), g)
    assert dp.preserved(g[1], parts("AC", "BC"), g)


@pytest.mark.parametrize("schema_parts, fds, lost_fds", [
    (("AB", "BC", "CD"), "A->B; B->C; C->D; D->A", ""),
    (("AC", "BC"), "AB->C; C->A", "AB->C"),
    (("AB", "CD"), "A->B; C->D", ""),
    (("AB", "AC"), "A->B; B->C", "B->C"),
    (("ABC", "CDE"), "AB->C; C->D; D->E; E->A", "E->A"),
])
def test_lost_and_preserving(dp, schema_parts, fds, lost_fds):
    f = parse(fds)
    assert fmt(dp.lost(parts(*schema_parts), f)) == fmt(parse(lost_fds))
    assert dp.is_dependency_preserving(parts(*schema_parts), f) is (lost_fds == "")


def test_the_lost_rule_in_sql(mysql, target):
    mysql.run_file(target / "0-zone_tables.sql").check()
    mysql.run(ZONES).check()
    assert not mysql.run("INSERT INTO zones VALUES ('N01', 'Naivasha');").ok, "zone -> town is kept by the key"
    assert not mysql.run("INSERT INTO addresses VALUES ('Moi Road', 'X99');").ok
    mysql.run("INSERT INTO addresses VALUES ('Kenyatta Avenue', 'N02');").check()  # nothing stops this
    got = mysql.run_file(target / "1-broken_rule.sql").check()
    assert got.columns == ["street", "town", "zones"]
    assert got.rows == [("Kenyatta Avenue", "Nakuru", "2")]
    mysql.run("INSERT INTO addresses VALUES ('Moi Road', 'N01'), ('Moi Road', 'E01');").check()
    assert [r[0] for r in mysql.run_file(target / "1-broken_rule.sql").check().rows] == ["Kenyatta Avenue", "Moi Road"]


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.D_TO_A_IS_PRESERVED, a.THE_SPLIT_IS_DEPENDENCY_PRESERVING, a.AB_TO_C_IS_PRESERVED,
            a.THIS_SPLIT_IS_LOSSLESS, a.THAT_SPLIT_IS_DEPENDENCY_PRESERVING, a.THAT_SPLIT_IS_LOSSLESS,
            a.EVERY_RELATION_HAS_A_LOSSLESS_DEPENDENCY_PRESERVING_3NF_SPLIT,
            a.EVERY_RELATION_HAS_A_LOSSLESS_DEPENDENCY_PRESERVING_BCNF_SPLIT] == [
        True, True, False, True, True, False, True, False]


def test_kata_what_each_table_knows(dp):
    f = parse("A->B; B->C; C->D; D->A")
    assert fmt(dp.project_fds(f, attrs("AC"))) == "A->C; C->A"
    assert fmt(dp.project_fds(parse("AB->C; C->A"), attrs("BC"))) == ""
    assert fmt(dp.project_fds(parse("A->B; B->C"), attrs("AC"))) == "A->C"
