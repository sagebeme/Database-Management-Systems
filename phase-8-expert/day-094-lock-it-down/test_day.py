"""Day 94: Lock It Down."""

import pytest

from coursekit import Postgres

ROLES = ("sacco_teller", "sacco_teller2", "sacco_auditor")


def drop_roles():
    server = Postgres()
    for role in ROLES:
        server.run(f"DROP ROLE IF EXISTS {role};")


@pytest.fixture
def clean_roles():
    """Roles belong to the whole server, not one database: start without them and remove them afterwards
    (after the test's database is gone)."""
    drop_roles()
    yield
    drop_roles()


@pytest.fixture
def pg(clean_roles, postgres, day):
    postgres.load(day / "setup.sql")
    return postgres


@pytest.fixture
def locked(pg, target):
    for name in ("0-roles.sql", "1-grants.sql", "2-row_security.sql"):
        pg.run_file(target / name).check()
    return pg


def as_role(pg, role):
    return Postgres(pg.database, user=role)


def test_roles(pg, target):
    pg.run_file(target / "0-roles.sql").check()
    rows = pg.run("SELECT rolname, rolcanlogin, rolsuper, rolcreatedb, rolcreaterole FROM pg_roles "
                  "WHERE rolname LIKE 'sacco%' ORDER BY 1;").check().rows
    assert rows == [(r, "t", "f", "f", "f") for r in sorted(ROLES)]


def test_grants(pg, target):
    pg.run_file(target / "0-roles.sql").check()
    pg.run_file(target / "1-grants.sql").check()
    teller, auditor = as_role(pg, "sacco_teller"), as_role(pg, "sacco_auditor")
    assert teller.run("SELECT id, name FROM members ORDER BY id;").check().rows[0] == ("1", "Wanjiku Kamau")
    for secret in ("phone", "id_number", "*"):
        result = teller.run(f"SELECT {secret} FROM members;")
        assert not result.ok and "permission denied" in result.stderr, f"a teller mustn't read members.{secret}"
    teller.run("INSERT INTO loans (member_id, amount) VALUES (2, 3000);").check()
    for change in ("UPDATE loans SET amount = 1;", "DELETE FROM loans;", "UPDATE members SET name = 'x';"):
        assert not teller.run(change).ok, f"a teller mustn't run {change}"
    assert auditor.run("SELECT * FROM members;").check().rows[2][3] == "28765432"
    assert len(auditor.run("SELECT * FROM loans;").check().rows) == 5
    for change in ("INSERT INTO loans (member_id, amount) VALUES (1, 5);", "DELETE FROM loans;",
                   "UPDATE members SET phone = '0';"):
        assert not auditor.run(change).ok, f"the auditor only reads: {change}"


def test_row_security(locked):
    teller, teller2, auditor = (as_role(locked, r) for r in ROLES)
    assert teller.run("SELECT id, amount FROM loans ORDER BY id;").check().rows == [("1", "50000"), ("3", "75000")]
    assert teller2.run("SELECT id, amount FROM loans ORDER BY id;").check().rows == [("2", "20000"), ("4", "10000")]
    assert len(auditor.run("SELECT * FROM loans;").check().rows) == 4
    assert len(locked.run("SELECT * FROM loans;").check().rows) == 4, "the owner still sees everything"
    teller.run("INSERT INTO loans (member_id, amount) VALUES (3, 4000);").check()
    assert teller.run("SELECT count(*) FROM loans;").check().rows == [("3",)]
    assert teller2.run("SELECT count(*) FROM loans;").check().rows == [("2",)]
    sneaky = teller.run("INSERT INTO loans (member_id, amount, officer) VALUES (3, 4000, 'sacco_teller2');")
    assert not sneaky.ok and "row-level security" in sneaky.stderr, "a teller can't file loans under someone else"


def test_audit(locked, target):
    locked.run_file(target / "3-audit.sql").check()
    teller = as_role(locked, "sacco_teller")
    teller.run("INSERT INTO loans (member_id, amount) VALUES (2, 3000);").check()
    locked.run("UPDATE loans SET amount = 55000 WHERE id = 1; DELETE FROM loans WHERE id = 4;").check()
    rows = locked.run("SELECT who, action, loan_id, old ->> 'amount', new ->> 'amount' FROM audit_log "
                      "ORDER BY id;").check().rows
    assert rows == [("sacco_teller", "INSERT", "5", "NULL", "3000"),
                    ("postgres", "UPDATE", "1", "50000", "55000"),
                    ("postgres", "DELETE", "4", "10000", "NULL")]
    assert locked.run("SELECT count(*) FROM audit_log WHERE at IS NULL;").check().rows == [("0",)]
    assert not teller.run("SELECT * FROM audit_log;").ok, "tellers have no rights on audit_log"
    assert not teller.run("INSERT INTO audit_log (who, action) VALUES ('x', 'y');").ok
    assert len(as_role(locked, "sacco_auditor").run("SELECT * FROM audit_log;").check().rows) == 3


def test_kata_append_only(locked, target):
    locked.run_file(target / "3-audit.sql").check()
    locked.run_file(target / "kata.sql").check()
    locked.run("UPDATE loans SET amount = 1 WHERE id = 1;").check()
    for change in ("UPDATE audit_log SET who = 'nobody';", "DELETE FROM audit_log;", "TRUNCATE audit_log;"):
        result = locked.run(change)
        assert not result.ok, f"even the owner mustn't be able to run {change}"
    assert locked.run("SELECT count(*) FROM audit_log;").check().rows == [("1",)]
    locked.run("INSERT INTO loans (member_id, amount) VALUES (1, 5);").check()
    assert locked.run("SELECT count(*) FROM audit_log;").check().rows == [("2",)], "adding still works"
