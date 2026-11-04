"""Day 65: Send Money.

The atomicity tests add a trigger that makes the last step of a transfer fail. If the earlier steps weren't in
the same transaction, their changes would stay behind.
"""

import pytest

from coursekit import load_module

WANJIKU, OTIENO, CHEBET, MUTUA, AKINYI = (f"2547{d}{d}00000{i}" for i, d in zip(range(1, 6), "12345"))
START = {WANJIKU: 5000, OTIENO: 1200, CHEBET: 0, MUTUA: 30000, AKINYI: 750}


@pytest.fixture
def wallet(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def balances(db):
    return {phone: int(b) for phone, b in db.run("SELECT phone, balance FROM accounts;").check().rows}


def transfers(db):
    return db.run("SELECT from_phone, to_phone, amount, reversed FROM transfers ORDER BY id;").check().rows


def send(db, sender, receiver, amount):
    return db.run(f"CALL SendMoney('{sender}', '{receiver}', {amount});")


def refused(result, message):
    return not result.ok and message in result.stderr and "45000" in result.stderr


def test_send_money(wallet, target):
    wallet.run_file(target / "0-send_money.sql").check()
    wallet.run_file(target / "0-send_money.sql").check()
    send(wallet, WANJIKU, CHEBET, 2000).check()
    send(wallet, CHEBET, AKINYI, 2000).check()
    assert balances(wallet) == {**START, WANJIKU: 3000, CHEBET: 0, AKINYI: 2750}
    assert transfers(wallet) == [(WANJIKU, CHEBET, "2000", "0"), (CHEBET, AKINYI, "2000", "0")]


def test_send_money_refusals(wallet, target):
    wallet.run_file(target / "0-send_money.sql").check()
    assert refused(send(wallet, CHEBET, WANJIKU, 1), "Insufficient funds")
    assert refused(send(wallet, OTIENO, WANJIKU, 1201), "Insufficient funds")
    assert refused(send(wallet, WANJIKU, "254700000000", 10), "No such account")
    assert refused(send(wallet, "254700000000", WANJIKU, 10), "No such account")
    assert refused(send(wallet, WANJIKU, OTIENO, 0), "Amount must be positive")
    assert refused(send(wallet, WANJIKU, OTIENO, -500), "Amount must be positive")
    assert balances(wallet) == START and transfers(wallet) == []
    send(wallet, OTIENO, WANJIKU, 1200).check()
    assert balances(wallet)[OTIENO] == 0, "every last shilling is fine"


def test_send_money_is_all_or_nothing(wallet, target):
    wallet.run_file(target / "0-send_money.sql").check()
    wallet.run("DELIMITER //\nCREATE TRIGGER break_777 BEFORE INSERT ON transfers FOR EACH ROW "
               "BEGIN IF NEW.amount = 777 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Disk full'; END IF; END //\n"
               "DELIMITER ;").check()
    assert refused(send(wallet, MUTUA, AKINYI, 777), "Disk full"), "pass the error on to the caller"
    assert balances(wallet) == START, "the money moved but the record failed: both updates must be undone"
    send(wallet, MUTUA, AKINYI, 778).check()
    assert balances(wallet) == {**START, MUTUA: 30000 - 778, AKINYI: 750 + 778}


def test_reverse_transfer(wallet, day, target):
    wallet.load(day / "solution" / "0-send_money.sql")
    wallet.run_file(target / "1-reverse_transfer.sql").check()
    wallet.run_file(target / "1-reverse_transfer.sql").check()
    send(wallet, MUTUA, OTIENO, 5000).check()
    send(wallet, WANJIKU, CHEBET, 3000).check()
    wallet.run("CALL ReverseTransfer(1);").check()
    assert balances(wallet) == {**START, WANJIKU: 2000, CHEBET: 3000}
    assert transfers(wallet) == [(MUTUA, OTIENO, "5000", "1"), (WANJIKU, CHEBET, "3000", "0")]
    assert refused(wallet.run("CALL ReverseTransfer(1);"), "Already reversed")
    assert refused(wallet.run("CALL ReverseTransfer(99);"), "No such transfer")
    send(wallet, CHEBET, AKINYI, 2500).check()
    assert refused(wallet.run("CALL ReverseTransfer(2);"), "Insufficient funds"), "Chebet spent it"
    assert balances(wallet) == {**START, WANJIKU: 2000, CHEBET: 500, AKINYI: 3250}


def test_reverse_transfer_is_all_or_nothing(wallet, day, target):
    wallet.load(day / "solution" / "0-send_money.sql")
    wallet.run_file(target / "1-reverse_transfer.sql").check()
    send(wallet, MUTUA, OTIENO, 5000).check()
    wallet.run("CREATE TRIGGER no_reversals BEFORE UPDATE ON transfers FOR EACH ROW "
               "SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Audit lock';").check()
    assert refused(wallet.run("CALL ReverseTransfer(1);"), "Audit lock")
    assert balances(wallet) == {**START, MUTUA: 25000, OTIENO: 6200}


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.A_POWER_CUT_AFTER_COMMIT_DOESNT_LOSE_THE_TRANSFER, a.A_TRANSFER_NEVER_HALF_HAPPENS,
            a.A_BALANCE_NEVER_GOES_BELOW_ZERO, a.TWO_TRANSFERS_AT_ONCE_DONT_SEE_EACH_OTHERS_HALF_DONE_WORK] == [
        "D", "A", "C", "I"]
    assert [a.CREATE_TABLE_INSIDE_A_TRANSACTION_COMMITS_IT, a.ROLLBACK_UNDOES_A_CREATE_TABLE,
            a.WITH_AUTOCOMMIT_ON_EACH_STATEMENT_IS_ITS_OWN_TRANSACTION] == [True, False, True]


def test_kata_pay_day(wallet, target):
    pay_day = load_module(target / "pay_day.py")
    conn = wallet.connect(autocommit=False)
    try:
        skipped = pay_day.pay_salaries(conn, MUTUA, [
            (WANJIKU, 10000), (OTIENO, 15000), ("254700000000", 1000), (CHEBET, 6000), (AKINYI, 4000)])
    finally:
        conn.close()
    assert skipped == ["254700000000", CHEBET]
    assert balances(wallet) == {**START, MUTUA: 1000, WANJIKU: 15000, OTIENO: 16200, AKINYI: 4750}, \
        "committed, and the unknown phone's payment didn't take Mutua's money"
    assert transfers(wallet) == [(MUTUA, WANJIKU, "10000", "0"), (MUTUA, OTIENO, "15000", "0"),
                                 (MUTUA, AKINYI, "4000", "0")]
