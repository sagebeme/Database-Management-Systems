"""Day 93: Never Lose Data."""

from datetime import date, timedelta

import pytest

from coursekit import Postgres, load_module, new_name

TABLES = ["members", "loans", "repayments"]


@pytest.fixture
def b(target):
    return load_module(target / "backup.py")


@pytest.fixture
def sacco(postgres, day):
    postgres.load(day / "setup.sql")
    return postgres


@pytest.fixture
def spare():
    """A database name for the restore, dropped afterwards."""
    name = new_name()
    yield name
    Postgres().run(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE);')


def test_dump_and_restore(b, sacco, spare, tmp_path):
    path = tmp_path / "sacco.dump"
    b.dump(sacco.database, path)
    assert path.stat().st_size > 1000
    assert path.read_bytes()[:5] == b"PGDMP", "pg_dump's custom format (-Fc)"
    b.restore(path, spare)
    copy = Postgres(spare)
    for table in TABLES:
        assert copy.run(f"SELECT count(*), sum(id) FROM {table};").check().rows == \
            sacco.run(f"SELECT count(*), sum(id) FROM {table};").check().rows
    assert not copy.run("INSERT INTO loans (member_id, amount, taken_on) VALUES (9999, 10, now());").ok, \
        "constraints come back too"
    assert copy.run("INSERT INTO members (name, phone) VALUES ('New', '254799999999') RETURNING id;").check().rows == [
        ("301",)], "so do the identity sequences"


def test_restore_refuses_an_existing_database(b, sacco, tmp_path):
    path = tmp_path / "sacco.dump"
    b.dump(sacco.database, path)
    with pytest.raises(RuntimeError):
        b.restore(path, sacco.database)
    assert sacco.run("SELECT count(*) FROM members;").check().rows == [("300",)]


def test_fingerprint(b, sacco):
    conn = sacco.connect()
    try:
        rows, checksum = b.fingerprint(conn, "members")
        assert rows == 300 and len(checksum) == 32
        assert b.fingerprint(conn, "members") == (rows, checksum), "the same data, the same fingerprint"
        sacco.run("UPDATE members SET name = 'Member 1 ' WHERE id = 1;").check()
        assert b.fingerprint(conn, "members")[1] != checksum, "one changed character changes it"
        with pytest.raises(ValueError):
            b.fingerprint(conn, "members; DROP TABLE loans")
    finally:
        conn.close()


def test_differences(b, sacco, spare, tmp_path):
    path = tmp_path / "sacco.dump"
    b.dump(sacco.database, path)
    b.restore(path, spare)
    a, c = sacco.connect(), Postgres(spare).connect()
    try:
        assert b.differences(a, c, TABLES) == [], "a good restore matches exactly"
        Postgres(spare).run("DELETE FROM repayments WHERE id = 7; UPDATE members SET phone = '0' WHERE id = 3;").check()
        assert b.differences(a, c, TABLES) == ["members", "repayments"]
    finally:
        a.close()
        c.close()


def test_answers(target):
    a = load_module(target / "answers.py")
    assert a.HOURS_LOST == 15
    assert [a.A_REPLICA_IS_A_BACKUP, a.A_BACKUP_YOU_HAVE_NEVER_RESTORED_IS_PROVEN,
            a.WITH_WAL_ARCHIVING_YOU_CAN_RESTORE_TO_ANY_MOMENT,
            a.ASYNCHRONOUS_REPLICATION_CAN_LOSE_COMMITTED_TRANSACTIONS] == [False, False, True, True]
    assert a.TIME_TO_RECOVER_IS_CALLED == "RTO"


def test_kata_keep(b):
    today = date(2026, 3, 15)                     # a Sunday
    nightly = {today - timedelta(days=n) for n in range(400)}
    kept = b.keep(nightly, today)
    daily = {today - timedelta(days=n) for n in range(7)}
    sundays = {date(2026, 3, 15), date(2026, 3, 8), date(2026, 3, 1), date(2026, 2, 22)}
    firsts = {date(2025, m, 1) for m in range(4, 13)} | {date(2026, m, 1) for m in (1, 2, 3)}
    assert kept == daily | sundays | firsts
    assert len(kept) == 7 + 3 + 11, "the 15th, the 8th and the 1st of March are counted once"
    assert date(2025, 3, 1) not in kept, "more than 364 days old"
    assert b.keep(set(), today) == set()
    assert b.keep({date(2026, 3, 16)}, today) == set(), "nothing from the future"


def test_kata_keep_with_gaps(b):
    today = date(2026, 3, 18)
    backups = {date(2026, 3, 18), date(2026, 3, 10), date(2026, 3, 8), date(2026, 2, 1), date(2026, 1, 3)}
    assert b.keep(backups, today) == {date(2026, 3, 18), date(2026, 3, 8), date(2026, 2, 1)}
