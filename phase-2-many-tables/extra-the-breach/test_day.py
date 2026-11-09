"""Extra: The Breach. Each clue runs your query on Soko Safi's logs, then changes the logs and runs it again, so the
query has to find the answer, not just say it. The final answers are stored as SHA-256 hashes."""

import hashlib

import pytest

from coursekit import load_module

# The same checks the solution passes, used to work out what each clue should return after the logs change.
REFERENCE = {
    "1-big_exports.sql": "SELECT id, username, at, row_count FROM exports "
                         "WHERE table_name = 'customers' AND row_count > 1000 ORDER BY at;",
    "2-whose_account.sql": "SELECT e.id, e.username, s.name, s.left_on FROM exports e "
                           "LEFT JOIN staff s ON s.username = e.username "
                           "WHERE e.table_name = 'customers' AND e.row_count > 1000 ORDER BY e.at;",
    "3-ghost_logins.sql": "SELECT l.username, l.ip, l.at FROM logins l JOIN staff s ON s.username = l.username "
                          "WHERE l.success AND DATE(l.at) > s.left_on ORDER BY l.at;",
    "4-same_ip.sql": "SELECT DISTINCT l.username FROM logins l WHERE l.success AND l.ip IN ("
                     "SELECT g.ip FROM logins g JOIN staff s ON s.username = g.username "
                     "WHERE g.success AND DATE(g.at) > s.left_on) "
                     "AND l.username NOT IN (SELECT username FROM staff WHERE left_on IS NOT NULL) ORDER BY 1;",
    "5-resets.sql": "SELECT account, reset_by, at FROM password_resets WHERE ticket_id IS NULL ORDER BY at;",
}

# What changes in the logs for the second run of each clue: one row that must show up, one that mustn't.
CHANGES = {
    "1-big_exports.sql": "INSERT INTO exports (username, table_name, row_count, at) VALUES "
                         "('akamau', 'customers', 1001, '2026-10-13 11:00:00'), "
                         "('akamau', 'orders', 9000, '2026-10-13 11:05:00'), "
                         "('dnjoroge', 'customers', 1000, '2026-10-13 11:10:00');",
    "2-whose_account.sql": "INSERT INTO exports (username, table_name, row_count, at) VALUES "
                           "('ghost_svc', 'customers', 2500, '2026-10-13 04:00:00'), "
                           "('pkiprop', 'customers', 3000, '2026-08-01 10:00:00');",
    "3-ghost_logins.sql": "INSERT INTO logins (username, ip, at, success) VALUES "
                          "('pkiprop', '105.160.4.9', '2026-09-10 20:00:00', 1), "
                          "('pkiprop', '105.160.4.9', '2026-08-15 17:30:00', 1), "
                          "('hachieng', '105.160.4.9', '2026-09-11 20:00:00', 0);",
    "4-same_ip.sql": "INSERT INTO logins (username, ip, at, success) VALUES "
                     "('dnjoroge', '41.90.66.12', '2026-10-13 07:00:00', 1), "
                     "('akamau', '41.90.66.12', '2026-10-13 07:05:00', 0), "
                     "('pkiprop', '105.160.4.9', '2026-09-10 20:00:00', 1), "
                     "('nwafula', '105.160.4.9', '2026-09-10 19:00:00', 1);",
    "5-resets.sql": "INSERT INTO password_resets (account, reset_by, at, ticket_id) VALUES "
                    "('akamau', 'bomondi', '2026-10-13 12:00:00', NULL), "
                    "('dnjoroge', 'bomondi', '2026-10-13 12:30:00', 4601);",
}

ANSWER_HASHES = {
    "ACCOUNT": "8ee52c0d1595428793093f4407768d7a21d34daa5535b3641f669be222bb3a65",
    "CULPRIT": "bd740bed896d9ef03481cdfd41747dfd58cc635dfb6769ee40829857ae9bf3f6",
    "WHEN": "8e053bea59a879e186caf2f4e40845f2c13c74660e4e7a6c90145d51fe2bb43d",
}


@pytest.fixture
def logs(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


@pytest.mark.parametrize("clue", sorted(REFERENCE))
def test_clue(logs, target, clue):
    for when in ("on the real logs", "after the logs change"):
        mine = logs.run_file(target / clue).check()
        expected = logs.run(REFERENCE[clue]).check()
        assert mine.rows, f"{clue} returns nothing {when}"
        assert mine.rows == expected.rows, f"{clue}: not the right rows {when} (check the columns and the order too)"
        logs.run(CHANGES[clue]).check()


def test_close_the_door(logs, target):
    logs.run("INSERT INTO staff VALUES ('swanjiku', 'Sarah Wanjiku', 'Sales', '2025-01-06', '2026-10-31', TRUE);").check()
    logs.run_file(target / "kata.sql").check()
    rows = logs.run("SELECT username, account_enabled FROM staff ORDER BY username;").check().rows
    left = {"hachieng", "jotieno", "pkiprop", "swanjiku"}
    for username, enabled in rows:
        want = "0" if username in left else "1"
        assert enabled == want, f"{username}'s account should be {'disabled' if want == '0' else 'left alone'}"


def normalise(name, value):
    text = str(value).strip().lower()
    if name == "WHEN" and len(text) == 19 and text.endswith(":00"):
        text = text[:16]
    return text


@pytest.mark.parametrize("name", sorted(ANSWER_HASHES))
def test_solved(target, name):
    given = getattr(load_module(target / "answers.py"), name)
    assert given is not None, f"{name} is still None"
    digest = hashlib.sha256(f"breach:{name}:{normalise(name, given)}".encode()).hexdigest()
    assert digest == ANSWER_HASHES[name], f"{name}: not this one. Follow the clues again."
