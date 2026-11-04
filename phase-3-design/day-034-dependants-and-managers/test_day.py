"""Day 34: Dependants and Managers."""

import pytest

from coursekit import er

QUERIES = ["1-employees_and_managers", "2-the_top", "3-team_sizes", "4-cover_counts", "kata"]
# A new hire under Lilian, a second top person, and a dependant for Samuel.
SHAKE_UP = """INSERT INTO employees VALUES (11, 'Brenda Wanjiru', 'Intern', 9), (12, 'Otieno Ouma', 'Board Chair', NULL);
UPDATE employees SET manager_id = 12 WHERE id = 1;
INSERT INTO dependants VALUES (10, 'Faith', 'spouse', '1988-08-08');"""


@pytest.fixture
def cover(mysql, day):
    mysql.load(day / "setup.sql")
    mysql.run_file(day / "solution" / "0-dependants.sql").check()
    mysql.load(day / "dependants.sql")
    return mysql


def test_dependants_table(mysql, day, target):
    mysql.load(day / "setup.sql")
    mysql.run_file(target / "0-dependants.sql").check()
    mysql.load(day / "dependants.sql")
    assert mysql.run("SELECT COUNT(*) FROM dependants WHERE name = 'Ivy';").check().rows == [("2",)], \
        "two Ivys, of different employees: the name alone isn't the key"
    assert not mysql.run("INSERT INTO dependants VALUES (1, 'Ivy', 'child', '2010-01-01');").ok, "(employee_id, name) is the key"
    assert not mysql.run("INSERT INTO dependants VALUES (99, 'Zed', 'child', '2010-01-01');").ok, "a real employee"
    assert not mysql.run("INSERT INTO dependants VALUES (3, 'Zed', 'cousin', '2010-01-01');").ok, "spouse or child"
    pk = mysql.run("SELECT column_name FROM information_schema.key_column_usage WHERE table_schema = DATABASE() "
                   "AND table_name = 'dependants' AND constraint_name = 'PRIMARY' ORDER BY ordinal_position;").check()
    assert pk.column(0) == ["employee_id", "name"]
    mysql.run("DELETE FROM employees WHERE id = 9;").check()
    assert mysql.run("SELECT COUNT(*) FROM dependants WHERE employee_id = 9;").check().rows == [("0",)], "ON DELETE CASCADE"


def test_diagram(target):
    d = er.load(target / "cover.mmd")
    owner = d.between("EMPLOYEE", "DEPENDANT")
    assert len(owner) == 1 and owner[0].identifying, "a weak entity hangs off an identifying relationship (--)"
    assert d.how_many("EMPLOYEE", per="DEPENDANT") == (1, 1)
    assert d.how_many("DEPENDANT", per="EMPLOYEE")[0] == 0
    assert d.keys("DEPENDANT") == {"employee_id", "name"}
    assert "employee_id" in d.keys("DEPENDANT", "FK")
    selfish = d.between("EMPLOYEE", "EMPLOYEE")
    assert len(selfish) == 1 and not selfish[0].identifying, "EMPLOYEE manages EMPLOYEE, non-identifying (..)"
    assert selfish[0].left_card == (0, 1) or selfish[0].right_card == (0, 1), "at most one manager"
    assert "manager_id" in d.keys("EMPLOYEE", "FK")


@pytest.mark.parametrize("name", QUERIES)
@pytest.mark.parametrize("shaken", [False, True], ids=["data", "shake-up"])
def test_against_reference(cover, day, target, name, shaken):
    if shaken:
        cover.run(SHAKE_UP).check()
    got = cover.run_file(target / f"{name}.sql").check()
    want = cover.run_file(day / "solution" / f"{name}.sql").check()
    assert got.columns == want.columns
    assert got.rows == want.rows


def test_known_answers(cover, target):
    def rows(name):
        return cover.run_file(target / f"{name}.sql").check().rows

    first = rows("1-employees_and_managers")
    assert len(first) == 10 and ("Grace Wambui", "NULL") in first and ("Lilian Achieng", "Joseph Otieno") in first
    assert rows("2-the_top") == [("Grace Wambui",)]
    assert rows("3-team_sizes") == [("Grace Wambui", "3"), ("Peter Kamau", "3"), ("Halima Abdi", "2"), ("Joseph Otieno", "1")]
    assert rows("4-cover_counts")[:3] == [("Peter Kamau", "3"), ("Fatuma Hassan", "2"), ("Grace Wambui", "2")]
    assert rows("4-cover_counts")[-1] == ("Samuel Kiprop", "0")
    assert ("Lilian Achieng", "Peter Kamau") in rows("kata") and len(rows("kata")) == 6
