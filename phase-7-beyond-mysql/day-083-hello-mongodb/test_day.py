"""Day 83: Hello, MongoDB."""

import re

import pymongo
import pytest

PROMPT = re.compile(r"^[\w.-]+> ?", re.M)


@pytest.fixture
def shule(mongo, day):
    mongo.run_file(day / "setup.js").check()
    return mongo


@pytest.fixture
def schools(shule, mongo_url):
    client = pymongo.MongoClient(mongo_url)
    yield client[shule.database].schools
    client.close()


def output(db, path):
    """What the script prints, without mongosh's prompts."""
    result = db.run_file(path)
    assert result.ok, result.stderr
    assert "Error" not in result.stdout, result.stdout
    return PROMPT.sub("", result.stdout).strip()


def same_as_solution(db, target, day, name):
    got = output(db, target / name)
    assert got, "the script printed nothing"
    assert got == output(db, day / "solution" / name)
    return got


def test_list_databases(shule, target):
    got = output(shule, target / "0-list_databases")
    assert "admin" in got and shule.database in got


def test_insert(shule, schools, target):
    output(shule, target / "1-insert")
    found = list(schools.find({"name": "Upendo Girls"}, {"_id": 0}))
    assert found == [{"name": "Upendo Girls", "county": "Kakamega", "students": 860, "category": "county"}]
    assert schools.count_documents({}) == 9


def test_all(shule, target, day, schools):
    got = same_as_solution(shule, target, day, "2-all")
    assert "Mlima High School" in got and "Stadi Technical" in got
    schools.insert_one({"_id": 9, "name": "Mpya School"})
    assert "Mpya School" in same_as_solution(shule, target, day, "2-all")


def test_match(shule, target, day, schools):
    got = same_as_solution(shule, target, day, "3-match")
    assert "St. Faith Girls" in got and "Kilima Day" in got and "Ziwa Boys" not in got
    schools.update_one({"_id": 3}, {"$set": {"county": "Kiambu"}})
    assert "Ziwa Boys" in same_as_solution(shule, target, day, "3-match")


def test_count(shule, target, schools):
    assert output(shule, target / "4-count") == "3"
    schools.delete_one({"_id": 1})
    assert output(shule, target / "4-count") == "2"


def test_update(shule, target, schools):
    output(shule, target / "5-update")
    assert sorted(d["_id"] for d in schools.find({"region": "Nairobi Metro"})) == [6, 8]
    assert schools.count_documents({"region": {"$exists": True}}) == 2
    assert schools.find_one({"_id": 6})["clubs"] == ["robotics", "chess"], "$set adds a field; it keeps the others"


def test_delete(shule, target, schools):
    output(shule, target / "6-delete")
    assert sorted(d["_id"] for d in schools.find()) == [1, 2, 3, 5, 6, 8]


def test_starts_with_st(shule, target, day, schools):
    got = same_as_solution(shule, target, day, "7-starts_with_st")
    assert "St. Faith Girls" in got and "St. Peter's Kapsabet" in got
    assert "Stadi Technical" not in got, "St. with the dot: Stadi doesn't count"
    assert "_id" not in got and "county" not in got, "names only"
    schools.insert_one({"_id": 9, "name": "Mt. St. Mary's", "county": "Kiambu"})
    assert "Mt. St. Mary" not in same_as_solution(shule, target, day, "7-starts_with_st")


def test_kata(shule, target, day, schools):
    got = same_as_solution(shule, target, day, "kata")
    assert got.index("Jiji Academy") < got.index("Mlima High School")
    assert "Ziwa Boys" not in got and "Stadi Technical" not in got and "_id" not in got
    schools.insert_one({"_id": 9, "name": "Kubwa Robotics", "students": 2000, "clubs": ["robotics"]})
    schools.insert_one({"_id": 10, "name": "Ndogo Chess", "students": 1000, "clubs": ["chess"]})
    got = same_as_solution(shule, target, day, "kata")
    assert got.index("Kubwa Robotics") < got.index("Jiji Academy")
    assert "Ndogo Chess" not in got, "more than 1,000"
