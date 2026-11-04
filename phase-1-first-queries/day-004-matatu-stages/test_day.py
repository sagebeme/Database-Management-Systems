"""Day 4: Matatu Stages."""

import pytest


@pytest.fixture
def stage(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def rows(db, path):
    return sorted(db.run_file(path).check().rows)


def test_cheap_routes(stage, target):
    result = stage.run_file(target / "0-cheap_routes.sql").check()
    assert result.columns == ["route_no", "fare_kes"]
    assert sorted(result.rows) == [("23", "50"), ("33", "70"), ("40", "60"), ("45", "40"), ("48", "70")]


def test_routes_to_ngong(stage, target):
    result = stage.run_file(target / "1-to_ngong.sql").check()
    assert result.columns == ["id", "route_no", "destination", "sacco", "fare_kes", "distance_km", "night_fare_kes"]
    assert sorted(result.rows) == [
        ("1", "11", "Ngong", "Neema Line", "100", "22.0", "150"),
        ("11", "52", "Ngong", "Kasi Sacco", "90", "22.0", "NULL"),
    ]


def test_routes_not_run_by_neema(stage, target):
    result = stage.run_file(target / "2-not_neema.sql").check()
    assert result.columns == ["route_no", "sacco"]
    assert [r for r, _ in sorted(result.rows)] == ["14", "23", "31", "33", "40", "42", "45", "52"]


def test_routes_without_night_service(stage, target):
    result = stage.run_file(target / "3-no_night_service.sql").check()
    assert result.columns == ["route_no", "destination"]
    assert sorted(result.rows) == [("25", "Rongai"), ("40", "Githurai"), ("45", "Westlands"), ("52", "Ngong")]


def test_long_routes(stage, target):
    result = stage.run_file(target / "4-long_routes.sql").check()
    assert result.columns == ["route_no", "distance_km"]
    assert sorted(result.rows) == [("11", "22.0"), ("14", "30.5"), ("31", "44.0"), ("52", "22.0"), ("57", "32.0")]


def test_long_routes_still_right_when_a_new_route_is_exactly_20_km(stage, target):
    stage.run("INSERT INTO routes VALUES (13, '60', 'Limuru', 'Kasi Sacco', 100, 20.0, NULL);").check()
    result = stage.run_file(target / "4-long_routes.sql").check()
    assert "60" not in result.column(0), "longer than 20 km means > 20, not >= 20"
    assert len(result.rows) == 5


def test_kata_shillings_per_km(stage, target):
    result = stage.run_file(target / "kata.sql").check()
    assert result.columns == ["route_no", "per_km"]
    assert sorted(result.rows) == [("23", "5.56"), ("25", "5.41"), ("45", "8.89")]
