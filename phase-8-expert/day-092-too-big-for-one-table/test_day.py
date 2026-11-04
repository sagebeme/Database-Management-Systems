"""Day 92: Too Big for One Table."""

import pytest

from coursekit import load_module


@pytest.fixture
def pg(postgres, day):
    postgres.load(day / "setup.sql")
    return postgres


@pytest.fixture
def parted(pg, target):
    pg.run_file(target / "0-partitioned.sql").check()
    return pg


def test_partitioned(parted):
    rows = parted.run("SELECT c.relname, pg_get_expr(c.relpartbound, c.oid) FROM pg_inherits i "
                      "JOIN pg_class c ON c.oid = i.inhrelid WHERE i.inhparent = 'payments'::regclass "
                      "ORDER BY 1;").check().rows
    assert rows == [
        ("payments_2026_01", "FOR VALUES FROM ('2026-01-01') TO ('2026-02-01')"),
        ("payments_2026_02", "FOR VALUES FROM ('2026-02-01') TO ('2026-03-01')"),
        ("payments_2026_03", "FOR VALUES FROM ('2026-03-01') TO ('2026-04-01')"),
        ("payments_default", "DEFAULT"),
    ]
    assert parted.run("SELECT pg_get_partkeydef('payments'::regclass);").check().rows == [("RANGE (paid_on)",)]
    key = parted.run("SELECT pg_get_constraintdef(oid) FROM pg_constraint WHERE conrelid = 'payments'::regclass "
                     "AND contype = 'p';").check().rows
    assert key == [("PRIMARY KEY (id, paid_on)",)]
    parted.run("INSERT INTO payments VALUES (1, '2026-02-14', '254711000001', 500), "
               "(2, '2026-07-01', '254711000001', 70);").check()
    assert parted.run("SELECT tableoid::regclass::text FROM payments ORDER BY id;").check().rows == [
        ("payments_2026_02",), ("payments_default",)], "each row lands in its month, or the default"
    assert not parted.run("INSERT INTO payments VALUES (3, NULL, '254711000001', 5);").ok


def test_copy_and_counts(parted, target):
    parted.run_file(target / "1-copy.sql").check()
    assert parted.run("SELECT count(*), sum(amount) FROM payments;").check().rows == \
        parted.run("SELECT count(*), sum(amount) FROM payments_old;").check().rows
    got = parted.run_file(target / "2-partition_counts.sql").check()
    assert got.columns == ["partition", "payments"]
    assert got.rows == [("payments_2026_01", "3100"), ("payments_2026_02", "2800"), ("payments_2026_03", "3100")]
    parted.run("INSERT INTO payments VALUES (99999, '2025-12-31', '254711000001', 5);").check()
    assert ("payments_default", "1") in parted.run_file(target / "2-partition_counts.sql").check().rows


def test_march_days_reads_one_partition(parted, target, day):
    parted.run_file(target / "1-copy.sql").check()
    got = parted.run_file(target / "3-march_days.sql").check()
    assert got.columns == ["paid_on", "total"]
    assert len(got.rows) == 31 and got.rows[0][0] == "2026-03-01" and got.rows[-1][0] == "2026-03-31"
    assert got.rows == parted.run("SELECT paid_on, sum(amount) FROM payments_old WHERE paid_on BETWEEN "
                                  "'2026-03-01' AND '2026-03-31' GROUP BY 1 ORDER BY 1;").check().rows
    query = "\n".join(l for l in (target / "3-march_days.sql").read_text().splitlines() if not l.startswith("--"))
    plan = "\n".join(r[0] for r in parted.run("EXPLAIN (COSTS OFF) " + query).check().rows)
    assert "payments_2026_03" in plan
    for other in ("payments_2026_01", "payments_2026_02", "payments_default"):
        assert other not in plan, f"partition pruning should skip {other}: compare paid_on itself with dates"


def test_archive_january(parted, target):
    parted.run_file(target / "1-copy.sql").check()
    parted.run_file(target / "4-archive_january.sql").check()
    assert parted.run("SELECT count(*) FROM payments;").check().rows == [("5900",)]
    assert parted.run("SELECT count(*) FROM payments_2026_01;").check().rows == [("3100",)], "the rows are kept"
    assert parted.run("SELECT count(*) FROM pg_inherits WHERE inhparent = 'payments'::regclass;").check().rows == [
        ("3",)]


@pytest.fixture
def sh(target):
    return load_module(target / "shards.py")


KEYS = [f"2547{n:08d}" for n in range(0, 40_000_000, 4001)]


def test_shard_for(sh):
    assert sh.shard_for("254711000001", 4) == sh.h("254711000001") % 4
    counts = [0] * 4
    for k in KEYS:
        counts[sh.shard_for(k, 4)] += 1
    assert all(abs(c - len(KEYS) / 4) < len(KEYS) * 0.05 for c in counts), "a good hash spreads keys evenly"


def test_moved_fraction(sh):
    assert sh.moved_fraction(KEYS, 4, 4) == 0
    assert 0.75 < sh.moved_fraction(KEYS, 4, 5) < 0.85, "going from 4 to 5 shards by modulo moves about 80% of keys"
    assert 0.45 < sh.moved_fraction(KEYS, 4, 8) < 0.55
    assert sh.moved_fraction([], 4, 5) == 0


def test_kata_ring(sh):
    ring = sh.Ring(replicas=100)
    with pytest.raises(LookupError):
        ring.node_for("254711000001")
    for node in ("db-nairobi", "db-mombasa", "db-kisumu", "db-eldoret"):
        ring.add(node)
    assert len(ring.points) == 400
    before = {k: ring.node_for(k) for k in KEYS}
    counts = {n: list(before.values()).count(n) for n in set(before.values())}
    assert len(counts) == 4 and min(counts.values()) > len(KEYS) * 0.15, "virtual nodes spread the keys"
    ring.add("db-nakuru")
    after = {k: ring.node_for(k) for k in KEYS}
    moved = [k for k in KEYS if before[k] != after[k]]
    assert all(after[k] == "db-nakuru" for k in moved), "keys only ever move to the new node"
    assert 0.12 < len(moved) / len(KEYS) < 0.30, "about a fifth of the keys move, not 80%"
    ring.remove("db-nakuru")
    assert {k: ring.node_for(k) for k in KEYS} == before, "removing it puts everything back"


def test_kata_ring_follows_the_rule(sh):
    ring = sh.Ring(replicas=3)
    ring.add("a")
    ring.add("b")
    points = sorted(ring.points)
    owner = {sh.h(f"{n}#{i}"): n for n in "ab" for i in range(3)}
    for k in KEYS[:500]:
        later = [p for p in points if p > sh.h(k)]
        assert ring.node_for(k) == owner[later[0] if later else points[0]]
