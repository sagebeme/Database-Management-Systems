# Day 84: MongoDB from Python

## The brief

Yesterday you typed queries into `mongosh`. The schools directory's website won't: its back end is Python, and every page view runs a query through **PyMongo**, the official driver. Today you'll write the functions behind the site: list, add, edit clubs, browse page by page, and the search form.

The search form brings the document world's version of SQL injection. Web frameworks turn JSON request bodies into Python dicts, and in MongoDB a dict *is* a query. If someone sends `{"county": {"$ne": null}}` and you pass the value straight through, they've changed your query.

## What you'll use

```python
from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27018")
schools = client.shule.schools          # database shule, collection schools (both made on first insert)

schools.insert_one({"name": "Upendo Girls", "county": "Kakamega"}).inserted_id
schools.find({"county": "Kiambu"})                      # a cursor: loop over it, or list(...) it
schools.find({}, {"name": 1})                           # projection: name (and _id)
schools.find_one({"_id": 3})                            # one dict, or None
schools.count_documents({"students": {"$gt": 1000}})
schools.update_many({"name": "Ziwa Boys"}, {"$set": {"clubs": ["rugby"]}}).modified_count
schools.delete_many({...}).deleted_count
```

It's the `mongosh` you know with Python dicts and snake_case names. Operators are strings: `{"$gt": 1000}`.

**Array updates**:

| | does |
|---|---|
| `{"$set": {"clubs": [...]}}` | replace the whole array |
| `{"$push": {"clubs": "drama"}}` | append, even if it's there already |
| `{"$addToSet": {"clubs": "drama"}}` | append only if it isn't there; makes the array if the field is missing |
| `{"$pull": {"clubs": "chess"}}` | remove every `"chess"` |

**Cursors** chain: `.sort("name", 1)` (or `.sort([("students", -1), ("name", 1)])`), `.skip(n)`, `.limit(n)`. Page `p` of size `k` is `.skip((p - 1) * k).limit(k)`, after a sort, or the pages can overlap.

**Operator injection**: when a value comes from outside, check its type before it goes into a query. A string can't carry an operator; a dict can. Numbers sent as strings fail quietly instead: `{"$gte": "1000"}` only matches fields that hold *strings*, so no school matches at all.

## Steps

```bash
mongosh --quiet mongodb://127.0.0.1:27018/shule < phase-7-beyond-mysql/day-083-hello-mongodb/setup.js
```

Then try things in a Python prompt with the client above.

1. `starter/schools.py`: `list_all`, `insert_school`, `set_clubs`, `add_club`, `remove_club`, `schools_with_club`, `page`.
2. `pytest phase-7-beyond-mysql/day-084-mongodb-from-python`

## The kata: The Search Form

In `starter/schools.py`, write `search(schools, county=None, min_students=None, club=None)`: build the query from whichever criteria were given, and refuse values of the wrong type before they reach MongoDB.

## When you're stuck

- **`list_all` returns `<pymongo.cursor.Cursor ...>`**: `find` returns a cursor. `list(...)` it.
- **`insert_school` returns an `InsertOneResult`**: the id is its `.inserted_id`.
- **`TypeError: document must be an instance of dict`**: `**fields` collects keyword arguments into a dict already. Pass `fields`, not `**fields`, to `insert_one`.
- **`add_club` makes duplicates**: `$push` always appends; `$addToSet` doesn't.
- **Page 2 repeats a name from page 1**: sort before you skip.
- **`search(min_students=True)` doesn't raise**: in Python, `True` is an `int`. Check for `bool` too.
- **`search(county={"$ne": None})` returns every school**: that's the injection. Check `isinstance(county, str)` first.
