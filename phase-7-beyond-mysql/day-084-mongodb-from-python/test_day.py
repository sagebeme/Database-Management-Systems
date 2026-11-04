"""Day 84: MongoDB from Python."""

import pymongo
import pytest

from coursekit import load_module

SCHOOLS = [
    {"_id": 1, "name": "Mlima High School", "county": "Nyeri", "students": 1450, "clubs": ["chess", "drama"]},
    {"_id": 2, "name": "St. Faith Girls", "county": "Kiambu", "students": 980, "clubs": ["music"]},
    {"_id": 3, "name": "Ziwa Boys", "county": "Kisumu", "students": 1210},
    {"_id": 4, "name": "Bahari Mixed Day", "county": "Mombasa", "students": 640, "clubs": []},
    {"_id": 5, "name": "Jiji Academy", "county": "Nairobi", "students": 1630, "clubs": ["robotics", "chess"]},
    {"_id": 6, "name": "Kilima Day", "county": "Kiambu", "students": 450},
    {"_id": 7, "name": "Stadi Technical", "county": "Nairobi", "students": 720, "clubs": ["robotics"]},
]


@pytest.fixture
def s(target):
    return load_module(target / "schools.py")


@pytest.fixture
def schools(mongo, mongo_url):
    client = pymongo.MongoClient(mongo_url)
    collection = client[mongo.database].schools
    collection.insert_many([dict(d) for d in SCHOOLS])
    yield collection
    client.close()


@pytest.fixture
def empty(mongo, mongo_url):
    client = pymongo.MongoClient(mongo_url)
    yield client[mongo.database].nothing_here
    client.close()


def test_list_all(s, schools, empty):
    assert s.list_all(schools) == SCHOOLS
    assert s.list_all(empty) == []


def test_insert_school(s, schools):
    new = s.insert_school(schools, name="Upendo Girls", county="Kakamega", students=860)
    assert schools.find_one({"_id": new}, {"_id": 0}) == {"name": "Upendo Girls", "county": "Kakamega", "students": 860}
    other = s.insert_school(schools, name="Bare")
    assert other != new and schools.find_one({"_id": other})["name"] == "Bare"


def test_set_clubs(s, schools):
    assert s.set_clubs(schools, "Ziwa Boys", ["football", "debate"]) == 1
    assert schools.find_one({"_id": 3})["clubs"] == ["football", "debate"]
    assert s.set_clubs(schools, "Nowhere", ["x"]) == 0
    schools.insert_one({"_id": 8, "name": "Ziwa Boys", "county": "Homa Bay"})
    assert s.set_clubs(schools, "Ziwa Boys", ["rugby"]) == 2
    assert schools.find_one({"_id": 1})["clubs"] == ["chess", "drama"]


def test_add_and_remove_club(s, schools):
    s.add_club(schools, "St. Faith Girls", "drama")
    s.add_club(schools, "St. Faith Girls", "drama")
    assert schools.find_one({"_id": 2})["clubs"] == ["music", "drama"], "no duplicates"
    s.add_club(schools, "Kilima Day", "football")
    assert schools.find_one({"_id": 6})["clubs"] == ["football"]
    s.remove_club(schools, "chess")
    assert schools.find_one({"_id": 1})["clubs"] == ["drama"]
    assert schools.find_one({"_id": 5})["clubs"] == ["robotics"]
    assert "clubs" not in schools.find_one({"_id": 3})


def test_schools_with_club(s, schools):
    assert s.schools_with_club(schools, "chess") == ["Jiji Academy", "Mlima High School"]
    assert s.schools_with_club(schools, "robotics") == ["Jiji Academy", "Stadi Technical"]
    assert s.schools_with_club(schools, "swimming") == []


def test_page(s, schools):
    assert s.page(schools, 1, 3) == ["Bahari Mixed Day", "Jiji Academy", "Kilima Day"]
    assert s.page(schools, 2, 3) == ["Mlima High School", "St. Faith Girls", "Stadi Technical"]
    assert s.page(schools, 3, 3) == ["Ziwa Boys"]
    assert s.page(schools, 4, 3) == []
    assert s.page(schools, 1, 100) == sorted(d["name"] for d in SCHOOLS)
    for bad in ((0, 3), (1, 0), (-1, 5)):
        with pytest.raises(ValueError):
            s.page(schools, *bad)


def test_kata_search(s, schools):
    assert s.search(schools) == ["Jiji Academy", "Mlima High School", "Ziwa Boys", "St. Faith Girls",
                                 "Stadi Technical", "Bahari Mixed Day", "Kilima Day"]
    assert s.search(schools, county="Kiambu") == ["St. Faith Girls", "Kilima Day"]
    assert s.search(schools, min_students=1000) == ["Jiji Academy", "Mlima High School", "Ziwa Boys"]
    assert s.search(schools, min_students=1450) == ["Jiji Academy", "Mlima High School"]
    assert s.search(schools, club="robotics", county="Nairobi") == ["Jiji Academy", "Stadi Technical"]
    assert s.search(schools, club="chess", min_students=1500) == ["Jiji Academy"]
    assert s.search(schools, county="Turkana") == []
    schools.insert_one({"_id": 9, "name": "Aa School", "county": "Kiambu", "students": 450})
    assert s.search(schools, county="Kiambu") == ["St. Faith Girls", "Aa School", "Kilima Day"]


@pytest.mark.parametrize("kwargs", [
    {"county": {"$ne": None}},
    {"club": {"$exists": True}},
    {"min_students": "1000"},
    {"min_students": True},
    {"min_students": 999.5},
    {"county": ["Kiambu"]},
])
def test_kata_search_refuses_odd_values(s, schools, kwargs):
    with pytest.raises(TypeError):
        s.search(schools, **kwargs)
