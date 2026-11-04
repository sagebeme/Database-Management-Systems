"""Day 53: Unique Users."""

import pytest

MEMBER = ("INSERT INTO chama_members (chama_id, name, phone, born_on, role, monthly_contribution) "
          "VALUES ({}, '{}', '{}', '{}', {}, {});")


def add(db, chama=1, name="Wanjiku", phone="254711000001", born="1990-05-01", role="'member'", pay=500):
    return db.run(MEMBER.format(chama, name, phone, born, role, pay))


@pytest.fixture
def pamoja(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def test_users(mysql, target):
    mysql.run_file(target / "0-users.sql").check()
    mysql.run("INSERT INTO users (email, name) VALUES ('wanjiku@pamoja.test', 'Wanjiku');").check()
    mysql.run("INSERT INTO users (email) VALUES ('otieno@pamoja.test');").check()
    mysql.run_file(target / "0-users.sql").check()
    assert mysql.run("SELECT id, email, name FROM users ORDER BY id;").check().rows == [
        ("1", "wanjiku@pamoja.test", "Wanjiku"), ("2", "otieno@pamoja.test", "NULL")], "running it again keeps the rows"
    assert not mysql.run("INSERT INTO users (email) VALUES ('wanjiku@pamoja.test');").ok, "emails never repeat"
    assert not mysql.run("INSERT INTO users (name) VALUES ('No Email');").ok, "email is required"


def test_country_users(mysql, target):
    mysql.run_file(target / "1-country_users.sql").check()
    mysql.run("INSERT INTO users (email) VALUES ('a@pamoja.test');").check()
    mysql.run("INSERT INTO users (email, country) VALUES ('b@pamoja.test', 'UG'), ('c@pamoja.test', 'SS');").check()
    assert mysql.run("SELECT email, country FROM users ORDER BY id;").check().rows == [
        ("a@pamoja.test", "KE"), ("b@pamoja.test", "UG"), ("c@pamoja.test", "SS")]
    assert not mysql.run("INSERT INTO users (email, country) VALUES ('d@pamoja.test', 'NG');").ok
    assert not mysql.run("INSERT INTO users (email, country) VALUES ('d@pamoja.test', NULL);").ok
    assert not mysql.run("INSERT INTO users (email) VALUES ('A@Pamoja.test');").ok, \
        "the collation compares emails without case"


def test_chama_members(mysql, target):
    mysql.run_file(target / "2-chama_members.sql").check()
    add(mysql).check()
    add(mysql, chama=2, name="Wanjiku", phone="254111000002", role="DEFAULT", pay=100000).check()
    assert mysql.run("SELECT role FROM chama_members WHERE chama_id = 2;").check().rows == [("member",)]
    assert not add(mysql, name="Otieno").ok, "a phone belongs to one member"
    assert not add(mysql, phone="254711000009").ok, "two Wanjikus in one chama get confused"
    assert not add(mysql, name="X", phone="0711000009").ok, "phones as 254..."
    assert not add(mysql, name="X", phone="254711000009", born="1899-12-31").ok, "born after 1900"
    assert not add(mysql, name="X", phone="254711000009", role="'patron'").ok
    assert not add(mysql, name="X", phone="254711000009", pay=99).ok, "contributions from 100"
    assert not add(mysql, name="X", phone="254711000009", pay=100001).ok, "up to 100,000"
    assert not mysql.run("INSERT INTO chama_members (chama_id, phone, born_on, monthly_contribution) "
                         "VALUES (1, '254711000009', '1990-01-01', 500);").ok, "name is required"
    mysql.run_file(target / "2-chama_members.sql").check()  # it starts over
    assert mysql.run("SELECT COUNT(*) FROM chama_members;").check().rows == [("0",)]


def test_duplicates(pamoja, target):
    assert pamoja.run_file(target / "3-duplicates.sql").check().rows == [
        ("wanjiku@pamoja.test", "3"), ("otieno@pamoja.test", "2")]
    pamoja.run("INSERT INTO signups VALUES (9, 'Akinyi@pamoja.test  ', 'A'), (10, 'mutua@pamoja.test', 'M'),"
               " (11, 'chebet@pamoja.test', 'C'), (12, 'CHEBET@pamoja.test', 'C');").check()
    assert pamoja.run_file(target / "3-duplicates.sql").check().rows == [
        ("chebet@pamoja.test", "3"), ("wanjiku@pamoja.test", "3"), ("akinyi@pamoja.test", "2"),
        ("mutua@pamoja.test", "2"), ("otieno@pamoja.test", "2")]


def test_clean_and_lock(pamoja, target):
    pamoja.run_file(target / "4-clean_and_lock.sql").check()
    assert pamoja.run("SELECT id, email, name FROM signups ORDER BY id;").check().rows == [
        ("1", "wanjiku@pamoja.test", "Wanjiku"), ("2", "otieno@pamoja.test", "Otieno"),
        ("4", "chebet@pamoja.test", "Chebet"), ("6", "mutua@pamoja.test", "Mutua"), ("8", "akinyi@pamoja.test", "Akinyi")]
    assert not pamoja.run("INSERT INTO signups VALUES (20, 'mutua@pamoja.test', 'Copy');").ok, "email is unique now"


def test_clean_keeps_the_first_even_if_it_is_messy(pamoja, target):
    pamoja.run("UPDATE signups SET email = '  Chebet@PAMOJA.test' WHERE id = 4;").check()
    pamoja.run("INSERT INTO signups VALUES (9, 'chebet@pamoja.test', 'Later');").check()
    pamoja.run_file(target / "4-clean_and_lock.sql").check()
    assert pamoja.run("SELECT id, email FROM signups WHERE name LIKE 'Chebet%' OR name = 'Later';").check().rows == [
        ("4", "chebet@pamoja.test")]


def test_kata_one_chair(mysql, day, target):
    mysql.load(day / "solution" / "2-chama_members.sql")
    mysql.run_file(target / "kata.sql").check()
    add(mysql, name="A", phone="254711000001", role="'chair'").check()
    add(mysql, name="B", phone="254711000002").check()
    add(mysql, name="C", phone="254711000003").check()
    add(mysql, name="D", phone="254711000004", role="'treasurer'").check()
    add(mysql, name="E", phone="254711000005", role="'treasurer'").check()
    add(mysql, chama=2, name="F", phone="254711000006", role="'chair'").check()
    assert not add(mysql, name="G", phone="254711000007", role="'chair'").ok, "chama 1 already has a chair"
    mysql.run("UPDATE chama_members SET role = 'member' WHERE name = 'A';").check()
    add(mysql, name="G", phone="254711000007", role="'chair'").check()
