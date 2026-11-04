"""Day 52: Capstone, The Agent's Ledger.

Your schema is tested on its own. The migration is compared with the reference migration, on the data as given
and on new rows. The reports run on the reference tables, so one mistake doesn't sink the rest.
"""

import pytest

from coursekit import load_module
from coursekit.fds import attrs, parse

CONTRACT = {
    "ledger_raw": {"code", "date_time", "till", "agent_name", "location", "phone", "customer_name", "txn_type",
                   "amount", "commission"},
    "agents": {"till", "name", "location"},
    "customers": {"phone", "name"},
    "transactions": {"code", "done_at", "till", "phone", "type", "amount", "commission"},
}
NEW_ROWS = """INSERT INTO ledger_raw VALUES
    ('TJZZ000001', '04/10/2026 08:05', '700001', ' Rongai Express ', 'Rongai', '+254 799 000 808', 'Halima Noor',
     ' WITHDRAWAL', '15,000', '80'),
    ('TJZZ000002', '04/10/2026 08:30', '512340', 'Mama Lucy Agencies', 'Kawangware', '0799000808', 'Halima Noor ',
     'Deposit', '1,000', '10');"""
DUMP = ["SELECT till, name, location FROM agents ORDER BY till;",
        "SELECT phone, name FROM customers ORDER BY phone;",
        "SELECT code, done_at, till, phone, type, amount, commission FROM transactions ORDER BY code;"]


def refused(db, sql):
    return not db.run(sql).ok


@pytest.fixture
def yours(mysql, day, target):
    mysql.load(day / "setup.sql")
    mysql.run_file(target / "0-schema.sql").check()
    return mysql


@pytest.fixture
def reference(mysql, day):
    mysql.load(day / "setup.sql")
    mysql.load(day / "solution" / "0-schema.sql")
    mysql.load(day / "solution" / "1-migrate.sql")
    return mysql


def test_schema_matches_the_contract(yours):
    rows = yours.run("SELECT table_name, column_name FROM information_schema.columns "
                     "WHERE table_schema = DATABASE();").check().rows
    found = {}
    for table, column in rows:
        found.setdefault(table.lower(), set()).add(column.lower())
    assert found == CONTRACT


def test_schema_rules(yours):
    yours.run("INSERT INTO agents VALUES ('512340', 'Mama Lucy Agencies', 'Kawangware');").check()
    yours.run("INSERT INTO customers VALUES ('254712000101', 'Wanjiku Kamau');").check()
    ok = "INSERT INTO transactions VALUES ('TJAAAAAAA{}', '2026-10-01 09:00:00', {}, {}, {}, {}, {});"
    yours.run(ok.format(1, "'512340'", "'254712000101'", "'Deposit'", 500, 10)).check()
    assert refused(yours, "INSERT INTO agents VALUES ('512340', 'Copy', 'Kawangware');"), "one row per till"
    assert refused(yours, "INSERT INTO agents VALUES ('512341', NULL, 'Kawangware');")
    assert refused(yours, "INSERT INTO customers VALUES ('0712000101', 'Wanjiku Kamau');"), "phones as 254..."
    assert refused(yours, "INSERT INTO customers VALUES ('254712000101', 'Copy');"), "one row per phone"
    assert refused(yours, ok.format(1, "'512340'", "'254712000101'", "'Deposit'", 500, 10)), "codes are unique"
    assert refused(yours, ok.format(2, "'999999'", "'254712000101'", "'Deposit'", 500, 10)), "a real agent"
    assert refused(yours, ok.format(3, "'512340'", "'254700000000'", "'Deposit'", 500, 10)), "a real customer"
    assert refused(yours, ok.format(4, "'512340'", "'254712000101'", "'Refund'", 500, 10)), "deposits and withdrawals only"
    assert refused(yours, ok.format(5, "'512340'", "'254712000101'", "NULL", 500, 10))
    assert refused(yours, ok.format(6, "'512340'", "'254712000101'", "'Deposit'", 0, 10)), "amounts above zero"
    assert refused(yours, ok.format(7, "'512340'", "'254712000101'", "'Deposit'", 500, -1)), "no negative commission"
    assert refused(yours, "INSERT INTO transactions VALUES ('TJAAAAAAA8', NULL, '512340', '254712000101', 'Deposit', 1, 1);")
    assert refused(yours, "DELETE FROM agents WHERE till = '512340';"), "an agent's transactions keep them"


def _dump(db):
    return [db.run(q).check().rows for q in DUMP]


@pytest.mark.parametrize("extra", ["", NEW_ROWS], ids=["as-given", "new-rows"])
def test_migrate(mysql, day, target, extra):
    mysql.load(day / "setup.sql")
    if extra:
        mysql.run(extra).check()
    mysql.load(day / "solution" / "0-schema.sql")
    mysql.run_file(target / "1-migrate.sql").check()
    yours = _dump(mysql)
    assert mysql.run("SELECT COUNT(*) FROM ledger_raw;").check().rows == [(str(24 + 2 * bool(extra)),)], \
        "leave ledger_raw alone"
    mysql.load(day / "setup.sql")
    if extra:
        mysql.run(extra).check()
    mysql.load(day / "solution" / "0-schema.sql")
    mysql.load(day / "solution" / "1-migrate.sql")
    want = _dump(mysql)
    for name, got, expected in zip(["agents", "customers", "transactions"], yours, want):
        assert got == expected, f"{name} doesn't match the cleaned ledger"


def test_migrate_spot_checks(mysql, day, target):
    mysql.load(day / "setup.sql")
    mysql.run(NEW_ROWS).check()
    mysql.load(day / "solution" / "0-schema.sql")
    mysql.run_file(target / "1-migrate.sql").check()
    assert mysql.run("SELECT * FROM agents WHERE till = '700001';").check().rows == [("700001", "Rongai Express", "Rongai")]
    assert mysql.run("SELECT * FROM customers WHERE phone = '254799000808';").check().rows == [
        ("254799000808", "Halima Noor")], "one customer, however the phone was written"
    assert mysql.run("SELECT done_at, type, amount FROM transactions WHERE code = 'TJZZ000001';").check().rows == [
        ("2026-10-04 08:05:00", "Withdrawal", "15000")]


def test_float(reference, target):
    assert reference.run_file(target / "2-float.sql").check().rows == [
        ("512340", "Mama Lucy Agencies", "16950", "5750", "185"),
        ("512377", "Baraka Mobile Shop", "21000", "200", "150"),
        ("600218", "Kilimani Cyber", "39000", "3750", "310")]
    reference.run("INSERT INTO agents VALUES ('700001', 'Rongai Express', 'Rongai');").check()
    assert reference.run_file(target / "2-float.sql").check().rows[-1] == ("700001", "Rongai Express", "0", "0", "0")


def test_rebuild(reference, day, target):
    got = reference.run_file(target / "3-rebuild.sql").check().rows
    assert got == reference.run_file(day / "solution" / "3-rebuild.sql").check().rows
    assert len(got) == 24
    assert got[0] == ("TJYA9FPUJV", "2026-10-01 09:02:00", "512377", "Baraka Mobile Shop", "Githurai 45",
                      "254701000606", "Hassan Ali", "Withdrawal", "200", "15")
    assert [r[0] for r in got[9:11]] == ["TJEJCAXQEZ", "TJY6AJT3CL"], "same minute: by code"


def closure(x, fds):
    result, changed = set(x), True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= result and not rhs <= result:
                result |= rhs
                changed = True
    return result


def test_answers(target):
    a = load_module(target / "answers.py")
    ours = parse("code -> date_time till phone txn_type amount commission; till -> agent_name location; "
                 "phone -> customer_name")
    assert isinstance(a.RAW_FDS, str), "RAW_FDS is a string like 'a -> b; c -> d'"
    theirs = parse(a.RAW_FDS)
    assert all(rhs <= closure(lhs, theirs) for lhs, rhs in ours), "some dependency is missing"
    assert all(rhs <= closure(lhs, ours) for lhs, rhs in theirs), "one of your dependencies doesn't hold"
    assert a.KEY == {"code"}
    assert a.HIGHEST_NF == "2NF"
    assert a.PARTS == {attrs("code date_time till phone txn_type amount commission"),
                       attrs("till agent_name location"), attrs("phone customer_name")}
    assert [a.COMMISSION_SHOULD_BE_WORKED_OUT_FROM_TODAYS_RATES_INSTEAD_OF_STORED,
            a.THE_NEW_TABLES_ARE_IN_BCNF] == [False, True]


def test_kata_regulars(reference, target):
    assert reference.run_file(target / "kata.sql").check().rows == [
        ("254110000404", "Mutua Musyoka", "3"), ("254712000101", "Wanjiku Kamau", "3"),
        ("254722000202", "Otieno Ouma", "2"), ("254745000505", "Akinyi Atieno", "2"),
        ("254768000707", "Njeri Wambui", "2")]
    reference.run("INSERT INTO transactions VALUES ('TJZZ000003', '2026-10-04 09:00:00', '600218', '254701000606', "
                  "'Deposit', 500, 10);").check()
    assert ("254701000606", "Hassan Ali", "2") in reference.run_file(target / "kata.sql").check().rows
