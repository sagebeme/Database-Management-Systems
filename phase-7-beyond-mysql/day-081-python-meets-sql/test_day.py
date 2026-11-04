"""Day 81: Python Meets SQL."""

import threading

import pytest

from coursekit import load_module


@pytest.fixture
def db(postgres, day):
    postgres.load(day / "setup.sql")
    return postgres


@pytest.fixture
def conn(db):
    c = db.connect()
    yield c
    c.close()


@pytest.fixture
def m(target):
    return load_module(target / "members.py")


def savings(db):
    return dict(db.run("SELECT phone, savings FROM members;").check().rows)


def test_find_member(m, conn):
    assert m.find_member(conn, "Wanjiku Kamau") == [(1, "Wanjiku Kamau", "Kiambu")]
    assert m.find_member(conn, "Nobody") == []
    assert m.find_member(conn, "Ng'ang'a Mwangi") == [(3, "Ng'ang'a Mwangi", "Nyeri")], \
        "a name with apostrophes must just work"


def test_find_member_is_not_fooled(m, conn, db, target):
    attack = "x'; DROP TABLE transfers; --"
    assert m.find_member(conn, attack) == []
    assert m.find_member(conn, "' OR '1'='1") == []
    assert db.run("SELECT count(*) FROM transfers;").ok, "the transfers table must survive"


@pytest.mark.passes_on_starter
def test_the_unsafe_one_breaks(m, conn):
    import psycopg
    with pytest.raises(psycopg.errors.SyntaxError):
        m.find_unsafe(conn, "Ng'ang'a Mwangi")


def test_answers(target, m, conn):
    a = load_module(target / "answers.py")
    assert isinstance(a.ATTACK, str), "ATTACK is a name, as a string"
    assert len(m.find_unsafe(conn, a.ATTACK)) == 7, "your ATTACK should make find_unsafe return all 7 members"
    assert [a.ESCAPING_QUOTES_BY_HAND_IS_AS_GOOD_AS_PARAMETERS, a.PARAMETERS_CAN_STAND_FOR_TABLE_OR_COLUMN_NAMES,
            a.PSYCOPG_3_SENDS_PARAMETERS_SEPARATELY_FROM_THE_SQL] == [False, False, True]


def test_add_member(m, conn, db):
    new = m.add_member(conn, "Halima Hassan", "254788000008", "Mombasa")
    assert new == 8
    assert db.run("SELECT name, county, savings FROM members WHERE id = 8;").check().rows == [
        ("Halima Hassan", "Mombasa", "0")]
    assert m.add_member(conn, "O'Neil Barasa", "254799000009", "Kakamega") == 9


def test_members_in(m, conn):
    assert m.members_in(conn, ["Kisumu"]) == ["Akinyi Atieno", "Otieno Ochieng"]
    assert m.members_in(conn, ["Kisumu", "Nairobi", "Kiambu"]) == [
        "Akinyi Atieno", "Otieno Ochieng", "Wanjiku Kamau", "Wanjiku Njeri"]
    assert m.members_in(conn, []) == []
    assert m.members_in(conn, ("Nyeri",)) == ["Ng'ang'a Mwangi"]
    assert m.members_in(conn, ["Kisumu') OR ('1'='1"]) == []


def test_transfer(m, conn, db):
    tid = m.transfer(conn, "254711000001", "254755000005", 2000)
    assert tid == 1
    s = savings(db)
    assert (s["254711000001"], s["254755000005"]) == ("40000", "5000")
    assert db.run("SELECT from_id, to_id, amount FROM transfers;").check().rows == [("1", "5", "2000")]
    assert m.transfer(conn, "254755000005", "254711000001", 5000) == 2


@pytest.mark.parametrize("args", [
    ("254755000005", "254711000001", 3001),
    ("254755000005", "254711000001", 0),
    ("254755000005", "254711000001", -10),
    ("254700000000", "254711000001", 100),
    ("254755000005", "254700000000", 100),
])
def test_transfer_refuses(m, conn, db, args):
    before = savings(db)
    with pytest.raises(ValueError):
        m.transfer(conn, *args)
    assert savings(db) == before
    assert db.run("SELECT count(*) FROM transfers;").check().rows == [("0",)]


def test_transfer_is_all_or_nothing(m, conn, db):
    db.run("""CREATE FUNCTION no_big() RETURNS trigger AS $$
              BEGIN IF NEW.amount > 10000 THEN RAISE EXCEPTION 'audit says no'; END IF; RETURN NEW; END $$
              LANGUAGE plpgsql;
              CREATE TRIGGER no_big BEFORE INSERT ON transfers FOR EACH ROW EXECUTE FUNCTION no_big();""").check()
    before = savings(db)
    with pytest.raises(Exception, match="audit says no"):
        m.transfer(conn, "254744000004", "254733000003", 20000)
    assert savings(db) == before, "the balance changes must roll back when the transfer record fails"


def test_transfers_at_once_dont_overspend(m, db):
    gate = threading.Barrier(4)
    outcome = []

    def pay():
        c = db.connect()
        try:
            gate.wait()
            m.transfer(c, "254722000002", "254711000001", 5000)
            outcome.append("ok")
        except ValueError:
            outcome.append("refused")
        finally:
            c.close()

    threads = [threading.Thread(target=pay) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(outcome) == ["ok", "ok", "ok", "refused"], "15,500 pays three transfers of 5,000, not four"
    assert savings(db)["254722000002"] == "500"


def test_kata_top_members(m, conn):
    assert m.top_members(conn, "savings", 3) == [
        ("Chebet Kiprop", "Uasin Gishu", 61000), ("Wanjiku Kamau", "Kiambu", 42000),
        ("Mutua Musyoka", "Machakos", 27500)]
    assert m.top_members(conn, "county", 2) == [
        ("Chebet Kiprop", "Uasin Gishu", 61000), ("Ng'ang'a Mwangi", "Nyeri", 8000)]
    assert [r[0] for r in m.top_members(conn, "name", 2)] == ["Wanjiku Njeri", "Wanjiku Kamau"]
    assert m.top_members(conn, "savings", 0) == []
    for bad in ("phone", "savings; DROP TABLE members", "savings DESC, (SELECT 1)", ""):
        with pytest.raises(ValueError):
            m.top_members(conn, bad, 3)
