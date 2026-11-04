"""Day 91: Reading Query Plans."""

import random
import re

import pytest

from coursekit import load_module

ONE_CUSTOMER = ("EXPLAIN (COSTS OFF) SELECT c.name, o.total FROM customers AS c JOIN orders AS o "
                "ON o.customer_id = c.id WHERE c.id = 42;")
SORTED = ("EXPLAIN (COSTS OFF) SELECT c.name, o.total FROM customers AS c JOIN orders AS o "
          "ON o.customer_id = c.id ORDER BY c.id;")
JOIN_NODE = re.compile(r"(Nested Loop|Hash Join|Merge Join)")


@pytest.fixture
def pg(postgres, day):
    postgres.load(day / "setup.sql")
    return postgres


def plan(result):
    return "\n".join(r[0] for r in result.check().rows)


def test_orders_index(pg, target):
    before = plan(pg.run("EXPLAIN (COSTS OFF) SELECT * FROM orders WHERE customer_id = 42;"))
    assert "Seq Scan on orders" in before
    pg.run_file(target / "0-orders_index.sql").check()
    after = plan(pg.run("EXPLAIN (COSTS OFF) SELECT * FROM orders WHERE customer_id = 42;"))
    assert "idx_orders_customer" in after and "Seq Scan" not in after


def test_explain(pg, target):
    got = plan(pg.run_file(target / "1-explain.sql"))
    assert "actual rows=" in got, "EXPLAIN ANALYZE runs the query and reports actual rows"
    assert "cost=" not in got and "actual time" not in got, "turn off COSTS and TIMING"
    assert "Execution Time" not in got, "turn off SUMMARY"
    assert "HashAggregate" in got or "GroupAggregate" in got
    assert JOIN_NODE.search(got)


def test_answers_match_the_real_plans(pg, target):
    a = load_module(target / "answers.py")
    report = plan(pg.run_file(target / "1-explain.sql"))
    assert a.COUNTY_REPORT_JOIN == JOIN_NODE.search(report).group(1), "read the join node off your plan"
    hashed = re.search(r"-> +Hash \(actual rows=(\d+)", report)
    assert hashed and a.ROWS_IN_THE_HASH == int(hashed.group(1))
    pg.run_file(target / "0-orders_index.sql").check()
    assert a.ONE_CUSTOMER_JOIN == JOIN_NODE.search(plan(pg.run(ONE_CUSTOMER))).group(1)
    assert a.SORTED_JOIN == JOIN_NODE.search(plan(pg.run(SORTED))).group(1)
    assert [a.A_HASH_JOIN_NEEDS_AN_EQUALITY_CONDITION, a.A_NESTED_LOOP_JOIN_CAN_JOIN_ON_ANY_CONDITION,
            a.EXPLAIN_WITHOUT_ANALYZE_RUNS_THE_QUERY] == [True, True, False]


@pytest.fixture
def j(target):
    return load_module(target / "joins.py")


def tables(seed, n_r=40, n_s=25, keys=10):
    rng = random.Random(seed)
    r = [{"id": i, "k": rng.choice(list(range(keys)) + [None])} for i in range(n_r)]
    s = [{"k": rng.choice(list(range(keys))), "v": f"v{i}"} for i in range(n_s)]
    return r, s


def canonical(rows):
    return sorted((tuple(sorted(row.items(), key=lambda kv: kv[0])) for row in rows), key=repr)


def brute(r, s, key):
    return [{**a, **b} for a in r for b in s if a[key] is not None and a[key] == b[key]]


ORDERS = [{"order": 1, "cust": 7}, {"order": 2, "cust": 9}, {"order": 3, "cust": 7}, {"order": 4, "cust": None}]
CUSTOMERS = [{"cust": 7, "name": "Wanjiku"}, {"cust": 8, "name": "Otieno"}, {"cust": 9, "name": "Chebet"}]
WANT = [{"order": 1, "cust": 7, "name": "Wanjiku"}, {"order": 2, "cust": 9, "name": "Chebet"},
        {"order": 3, "cust": 7, "name": "Wanjiku"}]


def test_nested_loop_join(j):
    rows, work = j.nested_loop_join(ORDERS, CUSTOMERS, "cust")
    assert canonical(rows) == canonical(WANT)
    assert work == 12
    for seed in range(5):
        r, s = tables(seed)
        rows, work = j.nested_loop_join(r, s, "k")
        assert canonical(rows) == canonical(brute(r, s, "k")) and work == len(r) * len(s)


def test_hash_join(j):
    rows, work = j.hash_join(ORDERS, CUSTOMERS, "cust")
    assert canonical(rows) == canonical(WANT)
    assert work == 7
    for seed in range(5):
        r, s = tables(seed)
        rows, work = j.hash_join(r, s, "k")
        assert canonical(rows) == canonical(brute(r, s, "k")) and work == len(r) + len(s)


@pytest.mark.parametrize("r_blocks, s_blocks, buffers, want", [
    (100, 50, 3, 100 + 100 * 50),
    (100, 50, 12, 100 + 10 * 50),
    (100, 50, 102, 150),
    (2000, 500, 52, 2000 + 40 * 500),
])
def test_block_nested_loop_cost(j, r_blocks, s_blocks, buffers, want):
    assert j.block_nested_loop_cost(r_blocks, s_blocks, buffers) == want


def test_kata_sort_merge_join(j):
    rows, work = j.sort_merge_join(ORDERS, CUSTOMERS, "cust")
    assert canonical(rows) == canonical(WANT)
    assert work == 6
    for seed in range(10):
        r, s = tables(seed, n_r=60, n_s=50, keys=8)
        rows, work = j.sort_merge_join(r, s, "k")
        assert canonical(rows) == canonical(brute(r, s, "k")), "keys that repeat on both sides join every pair"
        assert work <= len(r) + len(s), "a merge moves forward through each input once"
    assert j.sort_merge_join([], CUSTOMERS, "cust") == ([], 0)
