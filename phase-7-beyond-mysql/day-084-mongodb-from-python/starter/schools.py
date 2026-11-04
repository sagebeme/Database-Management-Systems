"""Day 84: MongoDB from Python, with PyMongo.

Every function takes a pymongo Collection, `schools`, holding documents like
    {"_id": ..., "name": "Mlima High School", "county": "Nyeri", "students": 1450, "clubs": ["chess", "drama"]}
Any field except _id and name can be missing.
"""


def list_all(schools):
    """Every document, as a list (empty if there are none)."""
    raise NotImplementedError("write this")


def insert_school(schools, **fields):
    """Insert a school with the given fields (insert_school(schools, name="X", county="Y")). Return the new _id."""
    raise NotImplementedError("write this")


def set_clubs(schools, name, clubs):
    """Replace the clubs of every school called `name` with the list `clubs`. Return how many were changed."""
    raise NotImplementedError("write this")


def add_club(schools, name, club):
    """Add one club to the school called `name`, unless it already has it (or has no clubs field yet: then it
    gets a list holding just this club)."""
    raise NotImplementedError("write this")


def remove_club(schools, club):
    """Take `club` out of every school's clubs."""
    raise NotImplementedError("write this")


def schools_with_club(schools, club):
    """The names of the schools that have `club`, alphabetical."""
    raise NotImplementedError("write this")


def page(schools, number, size):
    """Page `number` (1 for the first) of the schools sorted by name, `size` to a page: a list of names.
    ValueError if number or size is below 1."""
    raise NotImplementedError("write this")


def search(schools, county=None, min_students=None, club=None):
    """Kata: names of the schools matching every criterion that isn't None, biggest first, ties by name.
    The values come from a web form, so check them: county and club must be str, and min_students an int
    (not a bool); raise TypeError otherwise. A dict like {"$ne": None} passed as county must not get into
    the query."""
    raise NotImplementedError("write this")
