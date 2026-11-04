"""Day 96: Portfolio: SACCO Database. The tests are the client's acceptance checks."""

import threading
import time

import pytest

MEMBERS = [("Wanjiku Kamau", "254712345678"), ("Otieno Odhiambo", "254722000111"),
           ("Achieng Atieno", "254733222333"), ("Kiprono Kirui", "254110456789"),
           ("Fatuma Hassan", "254745678901")]


@pytest.fixture
def sacco(postgres, target):
    for name in ("schema.sql", "logic.sql", "reports.sql"):
        postgres.run_file(target / name).check()
    values = ", ".join(f"('{n}', '{p}')" for n, p in MEMBERS)
    postgres.run(f"INSERT INTO members (name, phone) VALUES {values};").check()
    return postgres


def one(db, sql):
    return db.run(sql).check().rows[0][0]


def fails(db, sql, words):
    result = db.run(sql)
    assert not result.ok, f"{sql} should have been refused"
    assert words in result.stderr.lower(), f"{sql} failed, but the message should mention {words!r}: {result.stderr}"


def test_members_are_checked(sacco):
    assert one(sacco, "SELECT count(*) FROM members;") == "5"
    assert one(sacco, "SELECT joined_on = CURRENT_DATE FROM members WHERE id = 1;") == "t"
    for phone in ("0712345678", "+254712345678", "25471234567", "254812345678"):
        assert not sacco.run(f"INSERT INTO members (name, phone) VALUES ('X', '{phone}');").ok, phone
    assert not sacco.run("INSERT INTO members (name, phone) VALUES ('Copy', '254712345678');").ok, "phones are unique"
    assert not sacco.run("INSERT INTO members (name, phone) VALUES ('  ', '254799999999');").ok, "a name is needed"


def test_ledger_rules(sacco):
    for bad in ("(1, 'deposit', 0)", "(1, 'deposit', -50)", "(1, 'gift', 50)", "(99, 'deposit', 50)"):
        assert not sacco.run(f"INSERT INTO ledger (member_id, kind, amount) VALUES {bad};").ok, bad


def test_deposit_and_withdraw(sacco):
    assert one(sacco, "SELECT deposit(1, 5000);") == "5000"
    assert one(sacco, "SELECT deposit(1, 2500);") == "7500"
    assert one(sacco, "SELECT withdraw(1, 1500);") == "6000"
    assert one(sacco, "SELECT savings(1);") == "6000"
    assert one(sacco, "SELECT savings(2);") == "0"
    fails(sacco, "SELECT withdraw(1, 6001);", "insufficient")
    assert one(sacco, "SELECT savings(1);") == "6000", "a refused withdrawal leaves nothing behind"
    fails(sacco, "SELECT deposit(42, 100);", "no such member")
    assert sacco.run("SELECT kind, amount FROM ledger ORDER BY id;").check().rows == [
        ("deposit", "5000"), ("deposit", "2500"), ("withdrawal", "1500")]


def test_two_withdrawals_at_once(sacco):
    sacco.run("SELECT deposit(1, 1000);").check()
    first = sacco.connect(autocommit=False)
    second = sacco.connect()
    try:
        first.execute("SELECT withdraw(1, 800);")
        outcome = {}

        def other_teller():
            try:
                second.execute("SELECT withdraw(1, 800);")
                outcome["result"] = "paid"
            except Exception as e:  # noqa: BLE001
                outcome["result"] = str(e)

        thread = threading.Thread(target=other_teller)
        thread.start()
        time.sleep(0.5)
        assert "result" not in outcome, "the second withdrawal must wait for the first: lock the member's row"
        first.commit()
        thread.join(10)
        assert "insufficient" in outcome.get("result", ""), outcome
    finally:
        first.close()
        second.close()
    assert one(sacco, "SELECT savings(1);") == "200"


def setup_savings(db):
    for member, amount in ((1, 10000), (2, 20000), (3, 15000), (4, 3000)):
        db.run(f"SELECT deposit({member}, {amount});").check()


def test_issue_loan(sacco):
    setup_savings(sacco)
    loan = one(sacco, "SELECT issue_loan(1, 25000, ARRAY[2, 3], ARRAY[10000, 5000]::bigint[]);")
    assert sacco.run(f"SELECT member_id, principal, balance, status FROM loans WHERE id = {loan};").check().rows == [
        ("1", "25000", "27500", "active")], "10% flat interest goes on at the start"
    assert sacco.run("SELECT loan_id, member_id, amount FROM guarantees ORDER BY member_id;").check().rows == [
        (loan, "2", "10000"), (loan, "3", "5000")]
    assert one(sacco, "SELECT free_savings(2);") == "10000"
    fails(sacco, "SELECT withdraw(2, 10001);", "insufficient")
    assert one(sacco, "SELECT withdraw(2, 10000);") == "10000", "free savings can still go"
    fails(sacco, "SELECT issue_loan(1, 100, '{}', '{}');", "active loan")


@pytest.mark.parametrize("call, words", [
    ("issue_loan(4, 9001, ARRAY[2], ARRAY[9000]::bigint[])", "limit"),
    ("issue_loan(1, 25000, ARRAY[2], ARRAY[10000]::bigint[])", "cover"),
    ("issue_loan(1, 20000, ARRAY[4], ARRAY[10000]::bigint[])", "guarantor"),
    ("issue_loan(1, 15000, ARRAY[1], ARRAY[5000]::bigint[])", "own"),
    ("issue_loan(1, 15000, ARRAY[2, 2], ARRAY[3000, 2000]::bigint[])", "twice"),
    ("issue_loan(1, 15000, ARRAY[2, 3], ARRAY[5000]::bigint[])", "length"),
    ("issue_loan(77, 100, '{}', '{}')", "no such member"),
])
def test_loans_refused(sacco, call, words):
    setup_savings(sacco)
    fails(sacco, f"SELECT {call};", words)
    assert one(sacco, "SELECT count(*) FROM loans;") == "0"
    assert one(sacco, "SELECT count(*) FROM guarantees;") == "0"


def test_no_guarantors_needed_when_savings_cover_it(sacco):
    setup_savings(sacco)
    loan = one(sacco, "SELECT issue_loan(2, 20000, '{}', '{}');")
    assert one(sacco, f"SELECT balance FROM loans WHERE id = {loan};") == "22000"
    fails(sacco, "SELECT issue_loan(3, 45001, ARRAY[2], ARRAY[30001]::bigint[]);", "limit")


def test_repay(sacco):
    setup_savings(sacco)
    loan = one(sacco, "SELECT issue_loan(1, 25000, ARRAY[2, 3], ARRAY[10000, 5000]::bigint[]);")
    assert one(sacco, f"SELECT repay({loan}, 7500);") == "20000"
    fails(sacco, f"SELECT repay({loan}, 20001);", "overpay")
    fails(sacco, "SELECT repay(999, 1);", "no such loan")
    assert one(sacco, "SELECT free_savings(2);") == "10000", "guarantees hold until the loan is cleared"
    assert one(sacco, f"SELECT repay({loan}, 20000);") == "0"
    assert one(sacco, f"SELECT status FROM loans WHERE id = {loan};") == "cleared"
    assert one(sacco, "SELECT free_savings(2);") == "20000", "a cleared loan frees its guarantors"
    assert sacco.run(f"SELECT amount FROM repayments WHERE loan_id = {loan} ORDER BY id;").check().rows == [
        ("7500",), ("20000",)]
    assert one(sacco, "SELECT issue_loan(1, 1000, '{}', '{}');") != loan, "a new loan once the old one is cleared"
    for bad in (f"UPDATE loans SET balance = -1 WHERE id = {loan};",
                f"UPDATE loans SET status = 'active' WHERE id = {loan};",
                f"INSERT INTO guarantees VALUES ({loan}, 4, 0);"):
        assert not sacco.run(bad).ok, f"the tables themselves must refuse: {bad}"


def test_member_summary(sacco):
    setup_savings(sacco)
    sacco.run("SELECT issue_loan(1, 25000, ARRAY[2, 3], ARRAY[10000, 5000]::bigint[]);").check()
    rows = sacco.run("SELECT member_id, name, savings, loan_balance, guaranteed, free_savings "
                     "FROM member_summary ORDER BY member_id;").check().rows
    assert rows == [
        ("1", "Wanjiku Kamau", "10000", "27500", "0", "10000"),
        ("2", "Otieno Odhiambo", "20000", "0", "10000", "10000"),
        ("3", "Achieng Atieno", "15000", "0", "5000", "10000"),
        ("4", "Kiprono Kirui", "3000", "0", "0", "3000"),
        ("5", "Fatuma Hassan", "0", "0", "0", "0"),
    ]


def test_monthly_flows(sacco):
    sacco.run("INSERT INTO ledger (member_id, kind, amount, at) VALUES "
              "(1, 'deposit', 500, '2026-01-05'), (1, 'deposit', 700, '2026-01-31 23:00'), "
              "(2, 'withdrawal', 200, '2026-01-20'), (2, 'deposit', 900, '2026-03-02');").check()
    rows = sacco.run("SELECT month, deposits, withdrawals FROM monthly_flows ORDER BY month;").check().rows
    assert rows == [("2026-01", "1200", "200"), ("2026-03", "900", "0")]


def test_kata_dividends(sacco, target):
    sacco.run_file(target / "kata.sql").check()
    sacco.run("INSERT INTO ledger (member_id, kind, amount, at) VALUES "
              "(1, 'deposit', 10000, '2025-03-01'), (1, 'withdrawal', 2000, '2025-12-31 23:59'), "
              "(1, 'deposit', 50000, '2026-01-01 00:00'), (2, 'deposit', 333, '2025-06-01'), "
              "(3, 'deposit', 400, '2025-06-01'), (3, 'withdrawal', 400, '2025-07-01'), "
              "(4, 'deposit', 1000, '2026-02-01');").check()
    assert sacco.run("SELECT * FROM dividends(2025, 9.5);").check().rows == [
        ("1", "Wanjiku Kamau", "760"), ("2", "Otieno Odhiambo", "31")]
    assert sacco.run("SELECT member_id, dividend FROM dividends(2026, 10);").check().rows == [
        ("1", "5800"), ("2", "33"), ("4", "100")]
    assert sacco.run("SELECT * FROM dividends(2024, 10);").check().rows == []
