"""Day 84: MongoDB from Python, with PyMongo.

Every function takes a pymongo Collection, `schools`, holding documents like
    {"_id": ..., "name": "Mlima High School", "county": "Nyeri", "students": 1450, "clubs": ["chess", "drama"]}
Any field except _id and name can be missing.
"""


def list_all(schools):
    """Every document, as a list (empty if there are none)."""
    return list(schools.find())


def insert_school(schools, **fields):
    """Insert a school with the given fields (insert_school(schools, name="X", county="Y")). Return the new _id."""
    return schools.insert_one(fields).inserted_id


def set_clubs(schools, name, clubs):
    """Replace the clubs of every school called `name` with the list `clubs`. Return how many were changed."""
    return schools.update_many({"name": name}, {"$set": {"clubs": list(clubs)}}).modified_count


def add_club(schools, name, club):
    """Add one club to the school called `name`, unless it already has it (or has no clubs field yet: then it
    gets a list holding just this club)."""
    schools.update_one({"name": name}, {"$addToSet": {"clubs": club}})


def remove_club(schools, club):
    """Take `club` out of every school's clubs."""
    schools.update_many({}, {"$pull": {"clubs": club}})


def schools_with_club(schools, club):
    """The names of the schools that have `club`, alphabetical."""
    return [d["name"] for d in schools.find({"clubs": club}, {"name": 1}).sort("name", 1)]


def page(schools, number, size):
    """Page `number` (1 for the first) of the schools sorted by name, `size` to a page: a list of names.
    ValueError if number or size is below 1."""
    if number < 1 or size < 1:
        raise ValueError("pages and sizes start at 1")
    cursor = schools.find({}, {"name": 1}).sort("name", 1).skip((number - 1) * size).limit(size)
    return [d["name"] for d in cursor]


def search(schools, county=None, min_students=None, club=None):
    """Kata: names of the schools matching every criterion that isn't None, biggest first, ties by name.
    The values come from a web form, so check them: county and club must be str, and min_students an int
    (not a bool); raise TypeError otherwise. A dict like {"$ne": None} passed as county must not get into
    the query."""
    query = {}
    if county is not None:
        if not isinstance(county, str):
            raise TypeError("county must be a string")
        query["county"] = county
    if club is not None:
        if not isinstance(club, str):
            raise TypeError("club must be a string")
        query["clubs"] = club
    if min_students is not None:
        if not isinstance(min_students, int) or isinstance(min_students, bool):
            raise TypeError("min_students must be a whole number")
        query["students"] = {"$gte": min_students}
    cursor = schools.find(query, {"name": 1}).sort([("students", -1), ("name", 1)])
    return [d["name"] for d in cursor]
