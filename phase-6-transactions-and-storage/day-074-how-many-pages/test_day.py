"""Day 74: How Many Pages."""

import pytest

from coursekit import load_module


@pytest.fixture
def pages(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def test_page_size(pages, target):
    assert pages.run_file(target / "0-page_size.sql").check().rows == [("16384",)]
    assert pages.run_file(target / "0-page_size.sql").columns == ["page_size"]


def test_table_sizes(pages, target, day):
    got = pages.run_file(target / "1-table_sizes.sql").check()
    assert got.columns == ["table_name", "table_rows", "data_pages", "index_pages"]
    want = pages.run_file(day / "solution" / "1-table_sizes.sql").check()
    assert got.rows == want.rows
    assert [r[0] for r in got.rows] == ["loans", "members"]
    assert got.rows[0][3] == "0", "loans has no secondary index"


def test_table_sizes_follows_the_tables(pages, target, day):
    pages.run("CREATE TABLE visits (id INT PRIMARY KEY, at DATETIME, KEY (at)); ANALYZE TABLE visits;").check()
    got = pages.run_file(target / "1-table_sizes.sql").check().rows
    assert [r[0] for r in got] == ["loans", "members", "visits"], "every table in the current database"


@pytest.fixture
def b(target):
    return load_module(target / "blocks.py")


def test_blocking_factor_and_file_blocks(b):
    assert b.blocking_factor(1024, 100) == 10
    assert b.blocking_factor(4096, 150) == 27
    assert b.blocking_factor(16384, 16384) == 1
    assert b.file_blocks(30000, 10) == 3000
    assert b.file_blocks(30001, 10) == 3001
    assert b.file_blocks(1, 27) == 1


def test_searches(b):
    assert b.linear_search_blocks(3000, True) == 1500
    assert b.linear_search_blocks(3000, False) == 3000
    assert b.linear_search_blocks(1, True) == 1
    assert b.binary_search_blocks(3000) == 12
    assert b.binary_search_blocks(1024) == 10
    assert b.binary_search_blocks(1025) == 11
    assert b.binary_search_blocks(1) == 1


@pytest.mark.parametrize("entries, fanout, levels", [
    (3000, 68, 2),
    (30000, 68, 3),
    (68, 68, 1),
    (69, 68, 2),
    (68 * 68, 68, 2),
    (68 * 68 + 1, 68, 3),
    (1, 500, 1),
    (10_000_000, 1200, 3),
])
def test_index_levels(b, entries, fanout, levels):
    assert b.index_levels(entries, fanout) == levels


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.BLOCKING_FACTOR, a.DATA_BLOCKS, a.INDEX_ENTRIES_PER_BLOCK, a.PRIMARY_INDEX_BLOCKS] == [10, 3000, 68, 45]
    assert [a.A_PRIMARY_INDEX_IS_SPARSE, a.A_SECONDARY_INDEX_ON_A_KEY_IS_DENSE,
            a.A_FILE_CAN_HAVE_MORE_THAN_ONE_PRIMARY_INDEX] == [True, True, False]


@pytest.mark.parametrize("args, want", [
    ((30000, 100, 1024, 9, 6, True), ("primary index", 3)),
    ((30000, 100, 1024, 9, 6, False), ("secondary index", 4)),
    ((100, 100, 1024, 9, 6, True), ("primary index", 2)),
    ((5, 100, 1024, 9, 6, False), ("linear", 1)),
    ((40, 100, 1024, 9, 6, False), ("linear", 2)),
    ((60, 100, 1024, 9, 6, True), ("primary index", 2)),
    ((40, 100, 1024, 9, 6, True), ("linear", 2)),
])
def test_kata_cheapest_lookup(b, args, want):
    assert b.cheapest_lookup(*args) == want
