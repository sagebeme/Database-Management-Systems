"""Day 5: M-Pesa Search."""

import pytest


@pytest.fixture
def statement(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def run(db, path, columns):
    result = db.run_file(path).check()
    assert result.columns == columns
    return sorted(result.rows)


def test_big_sends(statement, target):
    assert run(statement, target / "0-big_sends.sql", ["code", "counterparty", "amount"]) == [
        ("TC01AB4QR3", "Mary Achieng", "1200.00"),
        ("TC24LK8JH1", "Mary Achieng", "2500.00"),
    ]


def test_bills_and_tills(statement, target):
    rows = run(statement, target / "1-bills_and_tills.sql", ["code", "kind", "counterparty"])
    assert [code for code, *_ in rows] == ["TB28LM3PA2", "TC05GH2TY5", "TC15QW9ER8", "TC27MN3BV2", "TD01QA2WS4"]


def test_uses_in(target):
    text = (target / "1-bills_and_tills.sql").read_text().upper()
    assert " IN (" in text or " IN(" in text, "the task asks for IN (...) rather than OR"


def test_march_includes_the_last_evening_and_not_april(statement, target):
    rows = run(statement, target / "2-march.sql", ["code", "happened_at"])
    codes = [code for code, _ in rows]
    assert "TC31CX6ZA3" in codes, "31 March at 18:20 is still March"
    assert "TD01QA2WS4" not in codes, "1 April at midnight is April"
    assert "TB28LM3PA2" not in codes
    assert len(codes) == 11


def test_kplc_prepaid_and_postpaid(statement, target):
    assert run(statement, target / "3-kplc.sql", ["code", "counterparty", "amount"]) == [
        ("TB28LM3PA2", "KPLC PREPAID", "1500.00"),
        ("TC15QW9ER8", "KPLC POSTPAID", "2300.00"),
    ]


def test_neither_airtime_nor_small(statement, target):
    rows = run(statement, target / "4-not_small_airtime.sql", ["code", "kind"])
    assert len(rows) == 12
    assert all(kind != "Airtime" for _, kind in rows)


def test_neither_airtime_nor_small_catches_a_small_send(statement, target):
    statement.run("INSERT INTO transactions VALUES ('TC29TINY01', 'Sent', 'Kevin Otieno', 30.00, '2025-03-29 10:00:00');").check()
    codes = [code for code, _ in run(statement, target / "4-not_small_airtime.sql", ["code", "kind"])]
    assert "TC29TINY01" not in codes, "a 30-bob send is under 50 bob, so it's out"


def test_kata_brackets_matter(statement, target):
    assert run(statement, target / "kata.sql", ["code", "amount"]) == [
        ("TB21KQ8XZ1", "5000.00"),
        ("TC24LK8JH1", "2500.00"),
        ("TC31CX6ZA3", "4200.00"),
    ]
