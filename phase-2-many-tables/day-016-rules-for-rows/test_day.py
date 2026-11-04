"""Day 16: Rules for Rows. These tests try to break your tables: the database must say no."""


def create_twice(db, path):
    db.run_file(path).check()
    again = db.run_file(path)
    assert again.ok, f"the second run failed, so IF NOT EXISTS is missing:\n{again.stderr}"


def test_students_need_a_name(mysql, target):
    create_twice(mysql, target / "0-students.sql")
    mysql.run("INSERT INTO students (adm_no, name) VALUES (1001, 'Wanjiku');").check()
    refused = mysql.run("INSERT INTO students (adm_no, name) VALUES (1002, NULL);")
    assert not refused.ok and "cannot be null" in refused.stderr


def test_members_status_defaults_to_active(mysql, target):
    create_twice(mysql, target / "1-members.sql")
    mysql.run("INSERT INTO members (id, name) VALUES (1, 'Atieno');").check()
    assert mysql.run("SELECT status FROM members;").check().rows == [("active",)]
    refused = mysql.run("INSERT INTO members (id, name, status) VALUES (2, 'Nafula', NULL);")
    assert not refused.ok, "status must never be empty: NOT NULL as well as DEFAULT"


def test_customers_cannot_share_a_phone(mysql, target):
    create_twice(mysql, target / "2-customers.sql")
    mysql.run("INSERT INTO customers VALUES (1, 'Kamau', '254720000001');").check()
    refused = mysql.run("INSERT INTO customers VALUES (2, 'Njeri', '254720000001');")
    assert not refused.ok and "Duplicate entry" in refused.stderr
    mysql.run("INSERT INTO customers VALUES (3, 'Otieno', NULL), (4, 'Chebet', NULL);").check()


def test_products_number_themselves(mysql, target):
    create_twice(mysql, target / "3-products.sql")
    mysql.run("INSERT INTO products (name, price) VALUES ('Pen', 20); INSERT INTO products (name) VALUES ('Ruler');").check()
    assert mysql.run("SELECT id, name, price FROM products ORDER BY id;").check().rows == [
        ("1", "Pen", "20.00"), ("2", "Ruler", "0.00"),
    ]
    assert not mysql.run("INSERT INTO products (name) VALUES (NULL);").ok, "name is required"
    assert not mysql.run("INSERT INTO products (id, name) VALUES (1, 'Copy');").ok, "id is the primary key"
    key = mysql.run("SELECT column_name FROM information_schema.key_column_usage WHERE table_schema = DATABASE() "
                    "AND table_name = 'products' AND constraint_name = 'PRIMARY';").check().rows
    assert key == [("id",)]


def test_enrolments_once_per_unit(mysql, target):
    create_twice(mysql, target / "4-enrolments.sql")
    mysql.run("INSERT INTO enrolments VALUES (1001, 'SQL1001', '2025-01-10'), (1001, 'DBS2002', '2025-01-10'), "
              "(1002, 'SQL1001', '2025-01-11');").check()
    refused = mysql.run("INSERT INTO enrolments VALUES (1001, 'SQL1001', '2025-02-01');")
    assert not refused.ok and "Duplicate entry" in refused.stderr


def test_kata_which_id(mysql, target):
    mysql.run("CREATE TABLE products (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(60) NOT NULL, "
              "price DECIMAL(8, 2) NOT NULL DEFAULT 0) AUTO_INCREMENT = 41;").check()
    mysql.run("INSERT INTO products (name, price) VALUES ('Pen', 20), ('Ruler', 40);").check()
    result = mysql.run_file(target / "kata.sql").check()
    assert result.columns == ["new_id"]
    assert result.rows == [("43",)]
    assert mysql.run("SELECT name FROM products WHERE id = 43;").check().rows == [("Kalamu",)]
