"""Day 25: Who Can See What. Users belong to the whole server, so every test starts and
ends with the course users and riverwood_ops removed. The tests log in as each user."""

import pytest

from coursekit import MySQL

USERS = ["rw_admin", "rw_reader", "rw_app"]
OPS = "riverwood_ops"
REFERENCE = {
    "admin": "CREATE USER 'rw_admin'@'%' IDENTIFIED BY 'rw_admin_dev'; GRANT ALL PRIVILEGES ON *.* TO 'rw_admin'@'%';",
    "reader": f"CREATE DATABASE {OPS}; CREATE USER 'rw_reader'@'%' IDENTIFIED BY 'rw_reader_dev';"
              f" GRANT SELECT ON {OPS}.* TO 'rw_reader'@'%';",
    "app": "CREATE USER 'rw_app'@'%' IDENTIFIED BY 'rw_app_dev';"
           f" GRANT SELECT, INSERT, UPDATE ON {OPS}.* TO 'rw_app'@'%';",
}
OPS_TABLE = f"CREATE TABLE IF NOT EXISTS {OPS}.payouts (id INT PRIMARY KEY, amount INT); " \
            f"INSERT IGNORE INTO {OPS}.payouts VALUES (1, 5000), (2, 7500);"


def clean(server):
    drops = "".join(f"DROP USER IF EXISTS '{u}'@'%'; " for u in USERS)
    server.run(drops + f"DROP DATABASE IF EXISTS {OPS};").check()


@pytest.fixture
def server(mysql_server):
    clean(mysql_server)
    yield mysql_server
    clean(mysql_server)


def as_user(name, password=None):
    return MySQL(None, user=name, password=password or f"{name}_dev")


def test_create_admin(server, target):
    server.run_file(target / "0-create_admin.sql").check()
    server.run_file(target / "0-create_admin.sql").check()  # IF NOT EXISTS
    admin = as_user("rw_admin")
    admin.run(f"CREATE DATABASE {OPS}; CREATE TABLE {OPS}.t (id INT); DROP TABLE {OPS}.t;").check()


def test_create_reader(server, target):
    server.run_file(target / "1-create_reader.sql").check()
    server.run_file(target / "1-create_reader.sql").check()
    server.run(OPS_TABLE).check()
    reader = as_user("rw_reader")
    assert reader.run(f"SELECT SUM(amount) FROM {OPS}.payouts;").check().rows == [("12500",)]
    assert not reader.run(f"INSERT INTO {OPS}.payouts VALUES (3, 1);").ok, "the reader must not write"
    assert not reader.run(f"DROP TABLE {OPS}.payouts;").ok
    assert not reader.run("SELECT COUNT(*) FROM mysql.user;").ok, "only riverwood_ops, nothing else"


def test_show_grants(server, target):
    server.run(REFERENCE["admin"] + REFERENCE["reader"]).check()
    out = server.run_file(target / "2-show_grants.sql").check().stdout
    assert "Grants for rw_admin@%" in out and "Grants for rw_reader@%" in out
    assert out.index("rw_admin@%") < out.index("rw_reader@%"), "admin first, then reader"
    assert f"GRANT SELECT ON `{OPS}`.*" in out


def test_create_app_user(server, target):
    server.run(f"CREATE DATABASE {OPS};" + OPS_TABLE).check()
    server.run_file(target / "3-create_app_user.sql").check()
    server.run_file(target / "3-create_app_user.sql").check()
    app = as_user("rw_app")
    app.run(f"INSERT INTO {OPS}.payouts VALUES (3, 1200); UPDATE {OPS}.payouts SET amount = 1300 WHERE id = 3;").check()
    assert app.run(f"SELECT amount FROM {OPS}.payouts WHERE id = 3;").check().rows == [("1300",)]
    assert not app.run(f"DELETE FROM {OPS}.payouts WHERE id = 3;").ok, "no DELETE for the app"
    assert not app.run(f"DROP TABLE {OPS}.payouts;").ok


def test_revoke_insert(server, target):
    server.run(f"CREATE DATABASE {OPS};" + OPS_TABLE + REFERENCE["app"]).check()
    server.run_file(target / "4-revoke_insert.sql").check()
    app = as_user("rw_app")
    assert not app.run(f"INSERT INTO {OPS}.payouts VALUES (4, 1);").ok, "INSERT should be gone"
    app.run(f"UPDATE {OPS}.payouts SET amount = 5100 WHERE id = 1;").check()
    assert app.run(f"SELECT amount FROM {OPS}.payouts WHERE id = 1;").check().rows == [("5100",)]


def test_kata_change_the_locks(server, target):
    server.run(REFERENCE["reader"]).check()
    server.run_file(target / "kata.sql").check()
    assert not as_user("rw_reader").run("SELECT 1;").ok, "the old password must stop working"
    as_user("rw_reader", "rw_reader_new").run("SELECT 1;").check()
    assert "SELECT" in server.run("SHOW GRANTS FOR 'rw_reader'@'%';").check().stdout, "keep the privileges"
