"""Day 14: Capstone, County Weather Report.

Each answer is compared with a reference query on the same data, and some tests change the data
first, so an answer typed in by hand can't pass.
"""

import pytest

REFERENCE = {
    "0-average_highs": "SELECT county, ROUND(AVG(max_c), 1) AS avg_max FROM readings GROUP BY county ORDER BY AVG(max_c) DESC",
    "1-cool_season_top3": "SELECT county, ROUND(AVG(max_c), 1) AS avg_max FROM readings WHERE MONTH(recorded_on) IN (7, 8) "
                          "GROUP BY county ORDER BY AVG(max_c) DESC LIMIT 3",
    "2-record_highs": "SELECT county, MAX(max_c) AS hottest FROM readings GROUP BY county ORDER BY county",
    "3-wettest_months": "SELECT DATE_FORMAT(recorded_on, '%Y-%m') AS month, SUM(rain_mm) AS rain FROM readings "
                        "GROUP BY month ORDER BY rain DESC LIMIT 3",
    "4-gaps": "SELECT county, SUM(rain_mm IS NULL) AS missing FROM readings GROUP BY county "
              "HAVING SUM(rain_mm IS NULL) > 0 ORDER BY missing DESC, county",
    "5-swing": "SELECT county, MAX(max_c) - MIN(min_c) AS swing FROM readings GROUP BY county ORDER BY swing DESC, county",
    "6-climate_labels": "SELECT county, ROUND(AVG(max_c), 1) AS avg_max, "
                        "IF(AVG(max_c) >= 30, 'hot', IF(AVG(max_c) >= 24, 'warm', 'cool')) AS label "
                        "FROM readings GROUP BY county ORDER BY county",
    "7-report_lines": "SELECT CONCAT(county, ': ', FORMAT(SUM(rain_mm), 1), ' mm of rain in 2024') AS line "
                      "FROM readings GROUP BY county ORDER BY county",
    "kata": "SELECT county, recorded_on, min_c FROM readings ORDER BY min_c LIMIT 1",
}

# Changes that move answers around: a heatwave in Nyandarua, a wet week in Garissa,
# a lost reading in Mombasa, and a freezing night in Ol Kalou.
SHAKE_UP = """
UPDATE readings SET max_c = max_c + 12 WHERE county = 'Nyandarua' AND recorded_on BETWEEN '2024-07-01' AND '2024-08-31';
UPDATE readings SET rain_mm = 900 WHERE county = 'Garissa' AND recorded_on = '2024-01-10';
UPDATE readings SET rain_mm = NULL WHERE county = 'Mombasa' AND recorded_on < '2024-03-01';
UPDATE readings SET min_c = -1.5 WHERE county = 'Nyandarua' AND recorded_on = '2024-02-14';
"""


@pytest.fixture
def weather(mysql, day):
    mysql.load(day / "setup.sql")
    return mysql


def check(db, target, name):
    got = db.run_file(target / f"{name}.sql").check()
    want = db.run(REFERENCE[name] + ";").check()
    assert got.columns == want.columns
    assert got.rows == want.rows
    return got


@pytest.mark.parametrize("name", list(REFERENCE))
def test_answer(weather, target, name):
    check(weather, target, name)


@pytest.mark.parametrize("name", list(REFERENCE))
def test_answer_after_the_data_changes(weather, target, name):
    weather.run(SHAKE_UP).check()
    check(weather, target, name)


def test_spot_checks(weather, target):
    assert check(weather, target, "0-average_highs").rows[0] == ("Turkana", "36.0")
    assert check(weather, target, "3-wettest_months").rows[0][0] == "2024-05"
    assert check(weather, target, "kata").rows == [("Nyandarua", "2024-09-18", "5.3")]
