"""Day 50: Fourth Normal Form."""

import pytest

from coursekit import load_module
from coursekit.fds import attrs, parse
from coursekit.relational import make

OFFERS = [
    ("Achieng", "Maths", "English"), ("Achieng", "Maths", "Kiswahili"), ("Achieng", "Maths", "Dholuo"),
    ("Achieng", "Physics", "English"), ("Achieng", "Physics", "Kiswahili"), ("Achieng", "Physics", "Dholuo"),
    ("Baraka", "Chemistry", "English"), ("Baraka", "Chemistry", "Kiswahili"),
    ("Wanjiru", "Maths", "English"), ("Wanjiru", "Biology", "English"), ("Wanjiru", "Chemistry", "English"),
]
HEADING = ["tutor", "subject", "language"]


@pytest.fixture
def m(target):
    return load_module(target / "mvd.py")


@pytest.fixture
def tuition(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def test_split(tuition, target):
    tuition.run_file(target / "0-split.sql").check()
    assert tuition.run("SELECT COUNT(*) FROM tutor_subjects;").check().rows == [("6",)]
    assert tuition.run("SELECT COUNT(*) FROM tutor_languages;").check().rows == [("6",)]
    assert not tuition.run("INSERT INTO tutor_subjects VALUES ('Baraka', 'Chemistry');").ok, "each pair once"
    assert not tuition.run("INSERT INTO tutor_languages VALUES ('Baraka', 'English');").ok, "each pair once"


def test_split_on_other_data(mysql, day, target):
    mysql.load(day / "setup.sql")
    mysql.run("INSERT INTO tutor_offers VALUES ('Kiprop', 'History', 'English'), ('Kiprop', 'History', 'Kalenjin'),"
              " ('Kiprop', 'CRE', 'English'), ('Kiprop', 'CRE', 'Kalenjin');").check()
    mysql.run_file(target / "0-split.sql").check()
    assert mysql.run("SELECT subject FROM tutor_subjects WHERE tutor = 'Kiprop' ORDER BY 1;").check().rows == [
        ("CRE",), ("History",)]
    assert mysql.run("SELECT language FROM tutor_languages WHERE tutor = 'Kiprop' ORDER BY 1;").check().rows == [
        ("English",), ("Kalenjin",)]


def test_rebuild(tuition, day, target):
    tuition.run_file(day / "solution" / "0-split.sql").check()
    want = tuition.run("SELECT tutor, subject, language FROM tutor_offers ORDER BY 1, 2, 3;").check().rows
    assert tuition.run_file(target / "1-rebuild.sql").check().rows == want, "the join gives back every row, no more"


def test_achieng_adds_chemistry(tuition, day, target):
    tuition.run_file(day / "solution" / "0-split.sql").check()
    tuition.run_file(target / "2-achieng_adds_chemistry.sql").check()
    rows = tuition.run_file(day / "solution" / "1-rebuild.sql").check().rows
    assert [r for r in rows if r[0] == "Achieng" and r[1] == "Chemistry"] == [
        ("Achieng", "Chemistry", "Dholuo"), ("Achieng", "Chemistry", "English"), ("Achieng", "Chemistry", "Kiswahili")]
    assert len(rows) == 14
    assert tuition.run("SELECT COUNT(*) FROM tutor_languages;").check().rows == [("6",)], "her languages didn't change"


def test_holds_mvd(m):
    r = make(HEADING, OFFERS)
    assert m.holds_mvd(r, "tutor", "subject")
    assert m.holds_mvd(r, "tutor", "language"), "the complement holds too"
    assert not m.holds_mvd(r, "subject", "tutor")
    broken = make(HEADING, OFFERS[:-1])  # Wanjiru, Chemistry gone: still fine, she has one language
    assert m.holds_mvd(broken, "tutor", "subject")
    broken = make(HEADING, OFFERS[1:])  # Achieng teaches Maths in only two languages now
    assert not m.holds_mvd(broken, "tutor", "subject")
    assert m.holds_mvd(make(["A", "B"], [(1, 2), (1, 3)]), "A", "B"), "with nothing left over it's trivial"


def test_complement_and_trivial(m):
    s = attrs("ABCD")
    assert m.complement(s, attrs("A"), attrs("B")) == attrs("CD")
    assert m.is_trivial(s, attrs("AB"), attrs("B"))
    assert m.is_trivial(s, attrs("AB"), attrs("CD"))
    assert not m.is_trivial(s, attrs("A"), attrs("B"))


def test_violations_and_is_4nf(m):
    s = attrs("tutor subject language")
    mvds = [(attrs("tutor"), attrs("subject"))]
    assert m.violations(s, [], mvds) == mvds
    assert not m.is_4nf(s, [], mvds)
    assert m.is_4nf(attrs("ABC"), parse("A->BC"), [(attrs("A"), attrs("B"))]), "A is a key: allowed"
    assert m.violations(attrs("ABC"), parse("B->C"), []) == parse("B->C"), "an FD that breaks BCNF breaks 4NF"
    assert m.is_4nf(attrs("tutor subject"), [], []), "two attributes, no rule broken"


@pytest.mark.parametrize("schema, fds, mvds, want", [
    ("tutor subject language", "", [("tutor", "subject")], ["language tutor", "subject tutor"]),
    ("course teacher book", "", [("course", "book")], ["book course", "course teacher"]),
    ("ABCD", "A->B", [("A", "C")], ["AB", "AC", "AD"]),
    ("student course hobby phone", "", [("student", "course"), ("student", "hobby")],
     ["course student", "hobby student", "phone student"]),
    ("ABC", "A->BC", [("A", "B")], ["ABC"]),
])
def test_decompose_4nf(m, schema, fds, mvds, want):
    parts = m.decompose_4nf(attrs(schema), parse(fds), [(attrs(x), attrs(y)) for x, y in mvds])
    assert parts == [attrs(p) for p in want]


def test_answers(target):
    a = load_module(target / "answers.py")
    assert a.COURSE_PARTS == {frozenset({"course", "teacher"}), frozenset({"course", "book"})}
    assert (a.ROWS_IN_R_FOR_A_NEW_TEACHER, a.ROWS_SPLIT_FOR_A_NEW_TEACHER) == (3, 1)
    assert a.ROWS_OLD_TABLE_NEEDS_FOR_ACHIENGS_CHEMISTRY == 3
    assert [a.EVERY_FD_IS_AN_MVD, a.EVERY_MVD_IS_AN_FD, a.A_RELATION_IN_4NF_IS_IN_BCNF,
            a.A_BCNF_RELATION_IS_ALWAYS_IN_4NF, a.IF_X_MVD_Y_THEN_X_MVD_THE_REST] == [True, False, True, False, True]


def test_kata_find_the_mvds(m):
    assert m.mvds_in(make(HEADING, OFFERS)) == [("tutor", "language"), ("tutor", "subject")]
    clubs = make(["adm_no", "name", "club"], [(1, "Wanjiku", "Chess"), (1, "Wanjiku", "Drama"), (2, "Otieno", "Chess")])
    assert m.mvds_in(clubs) == [("adm_no", "club"), ("name", "club")], \
        "adm_no -> name is an FD, so it's left out; adm_no ->> club is a real MVD"
    assert m.mvds_in(make(HEADING, OFFERS[1:])) == []
