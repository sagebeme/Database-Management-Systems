"""Day 77: Where the Rows Live."""

import pytest

from coursekit import load_module

GROUP_BY_COUNTY = "SELECT county, COUNT(*) AS members, SUM(savings) AS savings FROM members GROUP BY county"
TOP_SAVERS = ("SELECT id, name, savings FROM members WHERE county = 'Nairobi' "
              "ORDER BY savings DESC LIMIT 10")


@pytest.fixture
def db(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def explain(db, sql):
    """The first row of EXPLAIN, as a dict."""
    result = db.run(f"EXPLAIN {sql.strip().rstrip(';')};").check()
    return dict(zip(result.columns, result.rows[0]))


def body(path):
    """A .sql file without its comment lines."""
    return "\n".join(line for line in path.read_text().splitlines() if not line.lstrip().startswith("--")).strip()


def indexes(db):
    rows = db.run("SELECT index_name, non_unique, GROUP_CONCAT(column_name ORDER BY seq_in_index) "
                  "FROM information_schema.statistics WHERE table_schema = DATABASE() AND table_name = 'members' "
                  "GROUP BY index_name, non_unique ORDER BY index_name;").check().rows
    return {name: (unique == "0", cols) for name, unique, cols in rows}


def test_unique_phone(db, target):
    db.run_file(target / "0-unique_phone.sql").check()
    assert indexes(db).get("uq_phone") == (True, "phone"), "a UNIQUE index called uq_phone on phone alone"
    clash = db.run("INSERT INTO members VALUES (99999, '254700007919', 'Copy', 'Nairobi', 0);")
    assert not clash.ok and "1062" in clash.stderr


def test_find_member_uses_only_the_index(db, target):
    db.run_file(target / "0-unique_phone.sql").check()
    sql = body(target / "1-find_member.sql")
    result = db.run(sql + ("" if sql.endswith(";") else ";")).check()
    assert result.columns == ["id", "phone"]
    assert result.rows == [("1", "254700007919")]
    plan = explain(db, sql)
    assert plan["key"] == "uq_phone"
    assert "Using index" in (plan["Extra"] or ""), \
        "uq_phone's leaves hold phone and the primary key, so id and phone need nothing else"


def test_county_index_covers_the_report(db, target):
    want = db.run(GROUP_BY_COUNTY + " ORDER BY county;").check().rows
    db.run_file(target / "2-county_index.sql").check()
    assert "idx_county_savings" in indexes(db)
    plan = explain(db, GROUP_BY_COUNTY)
    assert plan["key"] == "idx_county_savings"
    assert "Using index" in (plan["Extra"] or ""), "the index must hold every column the report reads"
    assert db.run(GROUP_BY_COUNTY + " ORDER BY county;").check().rows == want


def test_index_pages(db, target, day):
    db.run_file(target / "0-unique_phone.sql").check()
    db.run_file(target / "2-county_index.sql").check()
    db.run("ANALYZE TABLE members;").check()
    got = db.run_file(target / "3-index_pages.sql").check()
    assert got.columns == ["index_name", "pages"]
    assert got.rows == db.run_file(day / "solution" / "3-index_pages.sql").check().rows
    names = [r[0] for r in got.rows]
    assert names == ["PRIMARY", "idx_county_savings", "uq_phone"]
    pages = dict(got.rows)
    assert int(pages["PRIMARY"]) > int(pages["uq_phone"]), "the clustered index holds whole rows, so it's the biggest"


def test_answers(target, db):
    a = load_module(target / "answers.py")
    assert [a.A_SECONDARY_INDEX_LEAF_HOLDS_THE_PRIMARY_KEY, a.A_TABLE_CAN_HAVE_TWO_CLUSTERED_INDEXES,
            a.FINDING_A_WHOLE_ROW_THROUGH_A_SECONDARY_INDEX_SEARCHES_TWO_TREES,
            a.A_LONG_PRIMARY_KEY_MAKES_EVERY_SECONDARY_INDEX_BIGGER,
            a.RANDOM_UUID_PRIMARY_KEYS_INSERT_AS_CHEAPLY_AS_AUTO_INCREMENT] == [True, False, True, True, False]
    db.run("CREATE TABLE no_key (a INT, b INT); INSERT INTO no_key VALUES (1, 2); ANALYZE TABLE no_key;").check()
    names = {r[0] for r in db.run("SELECT index_name FROM mysql.innodb_index_stats WHERE database_name = DATABASE() "
                                  "AND table_name IN ('members', 'no_key');").check().rows}
    assert a.CLUSTERED_INDEX_NAME in names, "ask mysql.innodb_index_stats what members' clustered index is called"
    assert a.HIDDEN_CLUSTERED_INDEX_NAME in names - {"PRIMARY"}, "and what a table with no key gets"


def test_kata_top_savers(db, target):
    want = db.run(TOP_SAVERS + ";").check().rows
    db.run_file(target / "kata.sql").check()
    assert "idx_top_savers" in indexes(db)
    plan = explain(db, TOP_SAVERS)
    assert plan["key"] == "idx_top_savers"
    extra = plan["Extra"] or ""
    assert "filesort" not in extra, "the index should already be in savings order within Nairobi"
    assert "Using index" in extra, "id, name and savings should all come from the index"
    assert db.run(TOP_SAVERS + ";").check().rows == want
