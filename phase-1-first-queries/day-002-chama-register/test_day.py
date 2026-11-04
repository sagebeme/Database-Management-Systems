"""Day 2: The Chama Register."""

MEMBERS = [
    ("id", "int"),
    ("full_name", "varchar(100)"),
    ("phone", "varchar(12)"),
    ("joined_on", "date"),
    ("monthly_contribution", "decimal(8,2)"),
    ("is_official", "tinyint(1)"),
]

CONTRIBUTIONS = [
    ("member_id", "int"),
    ("amount", "decimal(10,2)"),
    ("paid_at", "datetime"),
    ("mpesa_code", "char(10)"),
]

MEMBERS_DDL = """CREATE TABLE members (id INT, full_name VARCHAR(100), phone VARCHAR(12), joined_on DATE,
    monthly_contribution DECIMAL(8,2), is_official BOOLEAN);"""


def columns_of(db, table: str) -> list[tuple[str, str]]:
    result = db.run(
        "SELECT column_name, column_type FROM information_schema.columns "
        f"WHERE table_schema = DATABASE() AND table_name = '{table}' ORDER BY ordinal_position;"
    ).check()
    return [(name, ctype) for name, ctype in result.rows]


def test_lists_tables(mysql, target):
    mysql.run("CREATE TABLE savings (id INT); CREATE TABLE loans (id INT);").check()
    result = mysql.run_file(target / "0-list_tables.sql").check()
    assert sorted(result.column(0)) == ["loans", "savings"]


def test_members_table_has_the_right_columns(mysql, target):
    mysql.run_file(target / "1-members_table.sql").check()
    assert columns_of(mysql, "members") == MEMBERS


def test_members_table_can_be_created_twice(mysql, target):
    mysql.run_file(target / "1-members_table.sql").check()
    again = mysql.run_file(target / "1-members_table.sql")
    assert again.ok, f"the second run failed, so IF NOT EXISTS is missing:\n{again.stderr}"
    assert columns_of(mysql, "members") == MEMBERS


def test_describes_members(mysql, target):
    mysql.run(MEMBERS_DDL).check()
    result = mysql.run_file(target / "2-describe_members.sql").check()
    assert result.columns[:2] == ["Field", "Type"]
    assert [(f, t) for f, t, *_ in result.rows] == MEMBERS


def test_contributions_table_has_the_right_columns(mysql, target):
    mysql.run_file(target / "3-contributions_table.sql").check()
    again = mysql.run_file(target / "3-contributions_table.sql")
    assert again.ok, f"the second run failed, so IF NOT EXISTS is missing:\n{again.stderr}"
    assert columns_of(mysql, "contributions") == CONTRIBUTIONS


def test_kata_table_count(mysql, target):
    mysql.run("CREATE TABLE a (x INT); CREATE TABLE b (x INT); CREATE TABLE c (x INT);").check()
    result = mysql.run_file(target / "kata.sql").check()
    assert result.columns == ["tables"]
    assert result.rows == [("3",)]


def test_kata_counts_only_this_database(mysql, target):
    result = mysql.run_file(target / "kata.sql").check()
    assert result.rows == [("0",)], "count only the current database's tables: WHERE table_schema = DATABASE()"
