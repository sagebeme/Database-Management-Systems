"""Day 95: The Data Warehouse."""

import pytest


@pytest.fixture
def pg(postgres, day):
    postgres.load(day / "setup.sql")
    return postgres


@pytest.fixture
def star(pg, target):
    pg.run_file(target / "0-star.sql").check()
    return pg


@pytest.fixture
def loaded(star, target):
    star.run_file(target / "1-etl.sql").check()
    return star


def columns(db, table):
    return db.run("SELECT column_name, data_type, is_nullable FROM information_schema.columns "
                  f"WHERE table_name = '{table}' ORDER BY ordinal_position;").check().rows


def test_star_schema(star):
    assert [c[0] for c in columns(star, "dim_date")] == ["date_key", "day", "month", "quarter", "year", "weekday",
                                                         "is_weekend"]
    shop = columns(star, "dim_shop")
    assert [c[0] for c in shop] == ["shop_key", "shop_id", "name", "county", "valid_from", "valid_to", "is_current"]
    assert [c[2] for c in shop] == ["NO", "NO", "NO", "NO", "NO", "YES", "NO"]
    assert [c[0] for c in columns(star, "dim_product")] == ["product_key", "product_id", "name", "category"]
    assert [c[0] for c in columns(star, "fact_sales")] == ["date_key", "shop_key", "product_key", "qty", "revenue"]
    refs = star.run("SELECT confrelid::regclass::text FROM pg_constraint WHERE conrelid = 'fact_sales'::regclass "
                    "AND contype = 'f' ORDER BY 1;").check().rows
    assert refs == [("dim_date",), ("dim_product",), ("dim_shop",)], "the fact table references each dimension"


def test_etl(loaded):
    assert loaded.run("SELECT count(*), min(day), max(day), sum(is_weekend::int) FROM dim_date;").check().rows == [
        ("365", "2026-01-01", "2026-12-31", "104")]
    assert loaded.run("SELECT month, quarter, year, weekday, is_weekend FROM dim_date WHERE date_key = 20260315;"
                      ).check().rows == [("3", "1", "2026", "Sunday", "t")]
    assert loaded.run("SELECT weekday FROM dim_date WHERE date_key = 20260101;").check().rows == [("Thursday",)]
    assert loaded.run("SELECT count(*) FROM dim_shop WHERE is_current AND valid_to IS NULL AND "
                      "valid_from = '2026-01-01';").check().rows == [("6",)]
    assert loaded.run("SELECT count(*) FROM dim_product;").check().rows == [("8",)]
    assert loaded.run("SELECT count(*), sum(qty), sum(revenue) FROM fact_sales;").check().rows == loaded.run(
        "SELECT count(*), sum(s.qty), sum(s.qty * p.price) FROM sales s JOIN products p ON p.id = s.product_id;"
    ).check().rows
    by_shop = ("SELECT {name}, sum({rev}) FROM {src} GROUP BY 1 ORDER BY 1;")
    assert loaded.run(by_shop.format(name="d.name", rev="f.revenue",
                                     src="fact_sales f JOIN dim_shop d USING (shop_key)")).check().rows == \
        loaded.run(by_shop.format(name="sh.name", rev="s.qty * p.price",
                                  src="sales s JOIN shops sh ON sh.id = s.shop_id JOIN products p ON p.id = s.product_id"
                                  )).check().rows, "each fact points at its own shop"


def same_as_solution(db, target, day, name):
    got = db.run_file(target / name).check()
    want = db.run_file(day / "solution" / name).check()
    assert got.columns == want.columns
    assert got.rows == want.rows
    return got


def test_rollup(loaded, target, day):
    got = same_as_solution(loaded, target, day, "2-rollup.sql")
    assert got.columns == ["county", "category", "revenue"]
    assert got.rows[-1] == ("NULL", "NULL", "1274740"), "the grand total comes last"
    subtotals = [r for r in got.rows if r[1] == "NULL" and r[0] != "NULL"]
    assert [r[0] for r in subtotals] == ["Kisumu", "Mombasa", "Nairobi", "Nakuru"]
    assert sum(int(r[2]) for r in subtotals) == 1274740
    loaded.run("UPDATE fact_sales SET revenue = revenue * 2 WHERE product_key = 1;").check()
    same_as_solution(loaded, target, day, "2-rollup.sql")


def test_weekends(loaded, target, day):
    got = same_as_solution(loaded, target, day, "3-weekends.sql")
    assert got.columns == ["category", "weekend_share"]
    assert len(got.rows) == 6
    loaded.run("UPDATE fact_sales SET revenue = 0 WHERE product_key IN (SELECT product_key FROM dim_product "
               "WHERE category = 'Oils') AND date_key IN (SELECT date_key FROM dim_date WHERE is_weekend);").check()
    got = same_as_solution(loaded, target, day, "3-weekends.sql")
    assert got.rows[-1] == ("Oils", "0.0")


def test_kata_scd2(loaded, target):
    loaded.run("UPDATE shops SET county = 'Kiambu' WHERE id = 5; UPDATE shops SET name = 'Pwani Super Mart' "
               "WHERE id = 3;").check()
    loaded.run_file(target / "kata.sql").check()
    rows = loaded.run("SELECT shop_id, name, county, valid_to = CURRENT_DATE - 1, valid_from = CURRENT_DATE, "
                      "is_current FROM dim_shop WHERE shop_id IN (3, 5) ORDER BY shop_id, shop_key;").check().rows
    assert rows == [
        ("3", "Pwani Mini Mart", "Mombasa", "t", "f", "f"),
        ("3", "Pwani Super Mart", "Mombasa", "NULL", "t", "t"),
        ("5", "Ngara Stores", "Nairobi", "t", "f", "f"),
        ("5", "Ngara Stores", "Kiambu", "NULL", "t", "t"),
    ]
    assert loaded.run("SELECT count(*), count(*) FILTER (WHERE is_current) FROM dim_shop;").check().rows == [("8", "6")]
    loaded.run_file(target / "kata.sql").check()
    assert loaded.run("SELECT count(*) FROM dim_shop;").check().rows == [("8",)], "nothing changed, nothing added"
    history = loaded.run("SELECT d.county, sum(f.revenue) > 0 FROM fact_sales f JOIN dim_shop d USING (shop_key) "
                         "WHERE d.shop_id = 5 GROUP BY 1;").check().rows
    assert history == [("Nairobi", "t")], "old sales still count for Nairobi, where the shop was then"
