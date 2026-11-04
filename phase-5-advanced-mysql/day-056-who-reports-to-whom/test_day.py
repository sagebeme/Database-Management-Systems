"""Day 56: Who Reports to Whom."""

import re

import pytest

# Two interns under Brian (one with a long name), Samuel moved under Faith, and a takings day after a gap.
SHAKE_UP = """INSERT INTO employees VALUES
    (16, 'Tom Barasa', 'Intern', 'Health', 20000, 8),
    (17, 'Wilhelmina Nyambura Wanjiku-Kariuki', 'Intern', 'Health', 20000, 16);
UPDATE employees SET manager_id = 7 WHERE name = 'Samuel Mutua';
INSERT INTO takings VALUES ('2026-03-17', 6100);"""
QUERIES = ["0-above_average", "1-chain_of_command", "2-org_chart", "3-team_size", "4-every_day", "kata"]


@pytest.fixture
def county(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def run(db, folder, name):
    return db.run_file(folder / f"{name}.sql").check().rows


def test_above_average(county, target):
    assert re.search(r"\bWITH\b", (target / "0-above_average.sql").read_text().split("this line.")[-1], re.I), \
        "write it with a CTE"
    assert run(county, target, "0-above_average") == [
        ("Amina Hassan", "Executive", "450000", "350000"), ("Peter Kamau", "Health", "300000", "156875"),
        ("John Mwangi", "Health", "220000", "156875"), ("Mercy Chebet", "Health", "180000", "156875"),
        ("David Otieno", "Health", "175000", "156875"), ("Faith Wairimu", "Health", "160000", "156875"),
        ("Grace Achieng", "Roads", "300000", "159000"), ("Hassan Ali", "Roads", "220000", "159000")]


def test_chain_of_command(county, target):
    assert run(county, target, "1-chain_of_command") == [
        ("0", "Brian Kiprono", "Clinical Officer"), ("1", "Faith Wairimu", "Medical Superintendent"),
        ("2", "Mercy Chebet", "Director Hospitals"), ("3", "John Mwangi", "Chief Officer Health"),
        ("4", "Peter Kamau", "CEC Health"), ("5", "Amina Hassan", "Governor")]


def test_org_chart(county, target):
    rows = run(county, target, "2-org_chart")
    assert len(rows) == 15
    assert rows[0] == ("Amina Hassan", "0", "Amina Hassan")
    assert ("Brian Kiprono", "5",
            "Amina Hassan > Peter Kamau > John Mwangi > Mercy Chebet > Faith Wairimu > Brian Kiprono") in rows


def test_team_size(county, target):
    assert run(county, target, "3-team_size") == [
        ("Amina Hassan", "14"), ("Peter Kamau", "7"), ("John Mwangi", "6"), ("Grace Achieng", "4"),
        ("Hassan Ali", "3"), ("Mercy Chebet", "3"), ("Faith Wairimu", "2"), ("David Otieno", "1"),
        ("Esther Wanjiru", "1")]


def test_every_day(county, target):
    rows = run(county, target, "4-every_day")
    assert len(rows) == 13
    assert rows[6] == ("2026-03-08", "0"), "Sunday is there, with 0"


@pytest.mark.parametrize("name", QUERIES)
def test_on_other_data(county, day, target, name):
    county.run(SHAKE_UP).check()
    assert run(county, target, name) == run(county, day / "solution", name)


def test_kata_lowest_common_boss(county, target):
    assert run(county, target, "kata") == [("John Mwangi",)]
    county.run(SHAKE_UP).check()
    assert run(county, target, "kata") == [("Faith Wairimu",)]
    county.run("UPDATE employees SET manager_id = 10 WHERE name = 'Brian Kiprono';").check()
    assert run(county, target, "kata") == [("Samuel Mutua",)], "if Brian reports to Samuel, Samuel is the answer"
