"""Day 82: Migrations."""

import shutil

import pytest

from coursekit import load_module

FLEET = """INSERT INTO vehicles (plate, owner) VALUES
    ('KDA 123A', 'Wanjiku Kamau (254711000001)'),
    ('KCB 456B', 'Otieno Ochieng (254722000002)'),
    ('KDD 789C', 'Wanjiku Kamau (254711000001)'),
    ('KBZ 010D', 'Chebet Kiprop (254700000004)');"""


@pytest.fixture
def mig(target):
    return load_module(target / "migrate.py")


@pytest.fixture
def conn(postgres):
    c = postgres.connect()
    yield c
    c.close()


def write(folder, files):
    folder.mkdir(exist_ok=True)
    for name, text in files.items():
        (folder / name).write_text(text)
    return folder


def tables(db):
    return [r[0] for r in db.run("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY 1;").check().rows]


# The runner, with migrations made up for the test.

def test_migration_files(mig, tmp_path):
    folder = write(tmp_path / "m", {"002_b.sql": "", "001_a.sql": "", "010_last_one.sql": "", "notes.txt": ""})
    assert [(v, n, p.name) for v, n, p in mig.migration_files(folder)] == [
        (1, "a", "001_a.sql"), (2, "b", "002_b.sql"), (10, "last_one", "010_last_one.sql")]
    assert mig.migration_files(write(tmp_path / "empty", {})) == []


@pytest.mark.parametrize("files", [
    {"001_a.sql": "", "001_b.sql": ""},
    {"1_a.sql": ""},
    {"001-a.sql": ""},
    {"001_Add Thing.sql": ""},
])
def test_migration_files_refuses(mig, tmp_path, files):
    with pytest.raises(mig.MigrationError):
        mig.migration_files(write(tmp_path / "m", files))


def test_applied_creates_the_table(mig, conn, postgres):
    assert mig.applied(conn) == set()
    assert "schema_migrations" in tables(postgres)
    assert mig.applied(conn) == set()


def test_migrate(mig, conn, postgres, tmp_path):
    folder = write(tmp_path / "m", {"001_a.sql": "CREATE TABLE a (x INT);",
                                     "002_b.sql": "CREATE TABLE b (y INT); INSERT INTO b VALUES (1), (2);"})
    assert mig.migrate(conn, folder) == [1, 2]
    assert tables(postgres) == ["a", "b", "schema_migrations"]
    assert mig.migrate(conn, folder) == [], "nothing runs twice"
    write(folder, {"003_c.sql": "ALTER TABLE a ADD COLUMN z TEXT;"})
    assert mig.migrate(conn, folder) == [3]
    rows = postgres.run("SELECT version, name, length(checksum) FROM schema_migrations ORDER BY 1;").check().rows
    assert rows == [("1", "a", "64"), ("2", "b", "64"), ("3", "c", "64")]
    assert mig.applied(conn) == {1, 2, 3}


def test_a_failure_stops_cleanly(mig, conn, postgres, tmp_path):
    folder = write(tmp_path / "m", {
        "001_a.sql": "CREATE TABLE a (x INT);",
        "002_b.sql": "CREATE TABLE b (y INT); INSERT INTO b VALUES ('not a number');",
        "003_c.sql": "CREATE TABLE c (z INT);",
    })
    with pytest.raises(mig.MigrationError, match="002_b.sql"):
        mig.migrate(conn, folder)
    assert tables(postgres) == ["a", "schema_migrations"], "001 stays; 002's CREATE TABLE b rolls back; 003 never runs"
    assert mig.applied(conn) == {1}
    write(folder, {"002_b.sql": "CREATE TABLE b (y INT); INSERT INTO b VALUES (7);"})
    assert mig.migrate(conn, folder) == [2, 3], "fix the file and run again"


# Your three migrations, run in order with psql (so they're checked even before the runner works).

@pytest.fixture
def run_migration(postgres, target):
    def run(name):
        postgres.run_file(target / "migrations" / name).check()
    return run


def columns(db, table):
    return db.run("SELECT column_name, data_type, is_nullable FROM information_schema.columns "
                  f"WHERE table_name = '{table}' ORDER BY ordinal_position;").check().rows


def test_001(postgres, run_migration):
    run_migration("001_create_vehicles.sql")
    assert columns(postgres, "vehicles") == [("id", "integer", "NO"), ("plate", "text", "NO"), ("owner", "text", "NO")]
    postgres.run(FLEET).check()
    assert not postgres.run("INSERT INTO vehicles (plate, owner) VALUES ('KDA 123A', 'X (1)');").ok, "plates are unique"


def test_002(postgres, run_migration):
    run_migration("001_create_vehicles.sql")
    postgres.run(FLEET).check()
    run_migration("002_add_seats.sql")
    assert postgres.run("SELECT DISTINCT seats FROM vehicles;").check().rows == [("14",)]
    postgres.run("INSERT INTO vehicles (plate, owner, seats) VALUES ('KDE 111E', 'A (2)', 33);").check()
    assert not postgres.run("INSERT INTO vehicles (plate, owner, seats) VALUES ('KDE 112E', 'A (2)', 0);").ok
    assert not postgres.run("INSERT INTO vehicles (plate, owner, seats) VALUES ('KDE 113E', 'A (2)', 71);").ok
    assert not postgres.run("INSERT INTO vehicles (plate, owner, seats) VALUES ('KDE 114E', 'A (2)', NULL);").ok


def test_003_moves_the_data(postgres, run_migration):
    run_migration("001_create_vehicles.sql")
    postgres.run(FLEET).check()
    run_migration("002_add_seats.sql")
    run_migration("003_owners_table.sql")
    assert postgres.run("SELECT id, name, phone FROM owners ORDER BY id;").check().rows == [
        ("1", "Chebet Kiprop", "254700000004"), ("2", "Wanjiku Kamau", "254711000001"),
        ("3", "Otieno Ochieng", "254722000002")]
    assert postgres.run("SELECT v.plate, o.name FROM vehicles v JOIN owners o ON o.id = v.owner_id "
                        "ORDER BY v.plate;").check().rows == [
        ("KBZ 010D", "Chebet Kiprop"), ("KCB 456B", "Otieno Ochieng"), ("KDA 123A", "Wanjiku Kamau"),
        ("KDD 789C", "Wanjiku Kamau")]
    assert [c[0] for c in columns(postgres, "vehicles")] == ["id", "plate", "seats", "owner_id"]
    assert columns(postgres, "vehicles")[3] == ("owner_id", "integer", "NO")
    assert not postgres.run("INSERT INTO vehicles (plate, owner_id) VALUES ('KDF 1F', 99);").ok, "a foreign key"
    assert not postgres.run("INSERT INTO owners (name, phone) VALUES ('Copy', '254711000001');").ok


def test_003_on_an_empty_fleet(postgres, run_migration):
    for name in ("001_create_vehicles.sql", "002_add_seats.sql", "003_owners_table.sql"):
        run_migration(name)
    assert tables(postgres) == ["owners", "vehicles"]


def test_your_runner_runs_your_migrations(mig, conn, postgres, target):
    assert mig.migrate(conn, target / "migrations") == [1, 2, 3]
    assert tables(postgres) == ["owners", "schema_migrations", "vehicles"]


# The kata.

def test_kata_edited_history(mig, conn, postgres, tmp_path):
    folder = write(tmp_path / "m", {"001_a.sql": "CREATE TABLE a (x INT);"})
    mig.migrate(conn, folder)
    write(folder, {"001_a.sql": "CREATE TABLE a (x INT, y INT);", "002_b.sql": "CREATE TABLE b (y INT);"})
    with pytest.raises(mig.MigrationError, match="001_a.sql"):
        mig.migrate(conn, folder)
    assert "b" not in tables(postgres), "check history before applying anything"
    write(folder, {"001_a.sql": "CREATE TABLE a (x INT);"})
    assert mig.migrate(conn, folder) == [2]


def test_kata_missing_file(mig, conn, tmp_path):
    folder = write(tmp_path / "m", {"001_a.sql": "CREATE TABLE a (x INT);"})
    mig.migrate(conn, folder)
    (folder / "001_a.sql").unlink()
    with pytest.raises(mig.MigrationError):
        mig.migrate(conn, folder)
    shutil.rmtree(folder)
