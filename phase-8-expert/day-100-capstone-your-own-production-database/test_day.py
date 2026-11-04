"""Day 100: Capstone: Your Own Production Database.

These tests don't know what your database is about. They check that it's built like a production
database: designed on paper first, created by migrations, constrained, indexed for its questions,
seeded, locked down, and able to undo its last migration."""

import re

import pytest

from coursekit import Postgres
from coursekit import er

HEADINGS = ["## Problem", "## Data model", "## Access patterns", "## Indexes", "## Backups and recovery",
            "## Security"]
BIG = 10_000
APP_ROLE = "capstone_app"


def drop_role():
    Postgres().run(f"DROP ROLE IF EXISTS {APP_ROLE};")


@pytest.fixture
def clean_role():
    drop_role()
    yield
    drop_role()


def migrations(target):
    return sorted((target / "migrations").glob("[0-9][0-9][0-9]*.sql"))


def migrate(db, target):
    for path in migrations(target):
        result = db.run_file(path)
        assert result.ok, f"{path.name} failed: {result.stderr}"


@pytest.fixture
def built(postgres, target):
    migrate(postgres, target)
    return postgres


@pytest.fixture
def seeded(built, target):
    result = built.run_file(target / "seed.sql")
    assert result.ok, f"seed.sql failed: {result.stderr}"
    built.run("ANALYZE;").check()
    return built


def tables(db):
    return db.run("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' "
                  "AND table_type = 'BASE TABLE' ORDER BY 1;").check().column(0)


def schema_snapshot(db):
    return db.run("SELECT table_name, column_name, data_type, is_nullable FROM information_schema.columns "
                  "WHERE table_schema = 'public' ORDER BY 1, 2;").check().rows


def has_real_sql(path):
    return any(line.strip() and not line.strip().startswith("--") for line in path.read_text().splitlines())


def test_design_doc(target):
    text = (target / "DESIGN.md").read_text(encoding="utf-8")
    for heading in HEADINGS:
        assert re.search(rf"^{re.escape(heading)}\b", text, re.M), f"DESIGN.md needs a section {heading!r}"
    assert "TODO" not in text, "DESIGN.md still has a TODO"
    diagram = er.load(target / "DESIGN.md")
    assert len(diagram.entities) >= 4, "the ER diagram should have at least four entities"
    assert len(diagram.relationships) >= 3, "and at least three relationships"
    for name, attrs in diagram.entities.items():
        assert attrs, f"give {name} its attributes in the diagram"
        assert any("PK" in a.keys for a in attrs.values()), f"{name} has no PK in the diagram"
    words = len(re.findall(r"\w+", text))
    assert words >= 300, f"DESIGN.md is {words} words; explain your decisions (300 at least)"


def test_migrations_build_the_schema(built, target):
    files = migrations(target)
    assert len(files) >= 3, "build the schema in at least three migrations"
    assert all(has_real_sql(f) for f in files), "a migration is only comments"
    assert len(tables(built)) >= 4


def test_diagram_matches_the_database(built, target):
    diagram = er.load(target / "DESIGN.md")
    in_db = set(tables(built))
    in_diagram = {name.lower() for name in diagram.entities}
    assert in_diagram == in_db, f"diagram only: {sorted(in_diagram - in_db)}; database only: {sorted(in_db - in_diagram)}"
    for name, attrs in diagram.entities.items():
        columns = set(built.run(f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' "
                                f"AND table_name = '{name.lower()}';").check().column(0))
        assert {a.lower() for a in attrs} == columns, f"{name}: the diagram and the table have different columns"


def test_constraints_and_indexes(built):
    no_pk = built.run("SELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace "
                      "WHERE n.nspname = 'public' AND c.relkind = 'r' AND NOT EXISTS (SELECT 1 FROM pg_constraint k "
                      "WHERE k.conrelid = c.oid AND k.contype = 'p');").check().column(0)
    assert no_pk == [], f"every table needs a primary key: {no_pk}"
    counts = dict(built.run("SELECT contype, count(*) FROM pg_constraint k JOIN pg_namespace n ON n.oid = k.connamespace "
                            "WHERE n.nspname = 'public' GROUP BY 1;").check().rows)
    assert int(counts.get("f", 0)) >= 3, "relate your tables with at least three foreign keys"
    assert int(counts.get("c", 0)) >= 3, "at least three CHECK constraints: let the database refuse bad data"
    assert int(counts.get("u", 0)) >= 1, "at least one UNIQUE constraint besides the keys"
    unindexed = built.run("""
        SELECT k.conrelid::regclass::text || ' (' || k.conname || ')'
        FROM pg_constraint k JOIN pg_namespace n ON n.oid = k.connamespace
        WHERE n.nspname = 'public' AND k.contype = 'f' AND NOT EXISTS (
            SELECT 1 FROM pg_index i
            WHERE i.indrelid = k.conrelid
              AND (i.indkey::int2[])[0:cardinality(k.conkey) - 1] @> k.conkey
              AND (i.indkey::int2[])[0:cardinality(k.conkey) - 1] <@ k.conkey)
        ORDER BY 1;""").check().column(0)
    assert unindexed == [], f"index every foreign key (its columns first in some index): {unindexed}"


def test_seed(seeded):
    sizes = {t: int(seeded.run(f'SELECT count(*) FROM "{t}";').check().rows[0][0]) for t in tables(seeded)}
    assert all(n > 0 for n in sizes.values()), f"seed every table: {sizes}"
    assert max(sizes.values()) >= BIG, f"seed at least one table with {BIG:,} rows, so the planner has to choose"


def query_files(target):
    return sorted((target / "queries").glob("*.sql"))


def test_queries(seeded, target):
    files = query_files(target)
    assert len(files) >= 5, "write at least five queries: the questions your database exists to answer"
    big = [t for t in tables(seeded) if int(seeded.run(f'SELECT count(*) FROM "{t}";').check().rows[0][0]) >= BIG]
    for path in files:
        text = path.read_text(encoding="utf-8")
        assert re.search(r"^-- question: \S", text, re.M), f"{path.name}: start with '-- question: ...'"
        result = seeded.run_file(path)
        assert result.ok, f"{path.name} failed: {result.stderr}"
        assert result.rows, f"{path.name} returns nothing on your seed data"
        if re.search(r"^-- full scan: \S", text, re.M):
            continue
        sql = "\n".join(line for line in text.splitlines() if not line.strip().startswith("--")).strip().rstrip(";")
        plan = "\n".join(seeded.run(f"EXPLAIN {sql};").check().column(0))
        for table in big:
            assert not re.search(rf"Seq Scan on {table}\b", plan), \
                f"{path.name} scans all of {table}: add an index, or say why with '-- full scan: ...'\n{plan}"


def statements(path):
    chunks = re.split(r"^-- expect error:.*$", path.read_text(encoding="utf-8"), flags=re.M)[1:]
    return [c.strip() for c in chunks if c.strip()]


def test_checks(seeded, target):
    checks = statements(target / "checks.sql")
    assert len(checks) >= 5, "write at least five statements your database must refuse"
    for sql in checks:
        result = seeded.run(sql)
        assert not result.ok, f"the database accepted something it should refuse:\n{sql}"


def test_security(clean_role, seeded, target):
    result = seeded.run_file(target / "security.sql")
    assert result.ok, f"security.sql failed: {result.stderr}"
    rows = seeded.run(f"SELECT rolcanlogin, rolsuper, rolcreatedb, rolcreaterole, rolbypassrls FROM pg_roles "
                      f"WHERE rolname = '{APP_ROLE}';").check().rows
    assert rows == [("t", "f", "f", "f", "f")], f"create a plain {APP_ROLE} role that can log in"
    owned = seeded.run(f"SELECT relname FROM pg_class WHERE relowner = '{APP_ROLE}'::regrole;").check().column(0)
    assert owned == [], f"the app mustn't own anything: {owned}"
    names = tables(seeded)
    readable = [t for t in names if seeded.run(
        f"SELECT has_table_privilege('{APP_ROLE}', '{t}', 'SELECT');").check().rows == [("t",)]]
    assert readable, "the app should be able to read something"
    for t in names:
        for power in ("TRUNCATE", "REFERENCES", "TRIGGER"):
            assert seeded.run(f"SELECT has_table_privilege('{APP_ROLE}', '{t}', '{power}');").check().rows == [("f",)], \
                f"the app doesn't need {power} on {t}"
    app = Postgres(seeded.database, user=APP_ROLE)
    assert app.run(f'SELECT 1 FROM "{readable[0]}" LIMIT 1;').ok
    assert not app.run(f'DROP TABLE "{names[0]}";').ok


def test_kata_undo_the_last_migration(postgres, target):
    files = migrations(target)
    for path in files[:-1]:
        postgres.run_file(path).check()
    before = schema_snapshot(postgres)
    postgres.run_file(files[-1]).check()
    assert schema_snapshot(postgres) != before
    down = target / "migrations" / "down" / files[-1].name
    result = postgres.run_file(down)
    assert result.ok, f"down/{files[-1].name} failed: {result.stderr}"
    assert schema_snapshot(postgres) == before, "undoing the last migration should leave the schema as it was before it"
    postgres.run_file(files[-1]).check()
    assert schema_snapshot(postgres) != before, "and it can be applied again"
