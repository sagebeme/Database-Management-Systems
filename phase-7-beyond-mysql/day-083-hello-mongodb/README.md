# Day 83: Hello, MongoDB

## The brief

A start-up wants a directory of Kenyan secondary schools. Some schools list their clubs, some don't; some will add a boarding fee, a motto or a photo gallery later; no two look quite alike. You could design tables for every possible field, or store each school as one self-contained **document** and let each have whatever fields it has.

That's **MongoDB**, the most widely used **document database**: no tables, no fixed columns, no joins by default. You've spent 82 days learning why relational databases work the way they do. Now you'll see what you gain and what you give up when a database doesn't.

## What you'll use

| Relational | MongoDB |
|---|---|
| database | database |
| table | **collection** |
| row | **document** (JSON-like, stored as BSON) |
| column | field (each document has its own) |
| primary key | `_id` (made for you if you don't give one) |

**The shell**, `mongosh`, is a JavaScript prompt:

```js
show dbs                                   // list databases
use shule                                  // switch to (or start) a database: it's created by the first insert
db.schools.insertOne({ name: "Mlima High School", county: "Nyeri", students: 1450 })
db.schools.find()                          // everything
db.schools.find({ county: "Kiambu" })      // where county = 'Kiambu'
db.schools.find({}, { _id: 0, name: 1 })   // projection: only the name
db.schools.countDocuments({ category: "national" })
db.schools.updateMany({ county: "Nairobi" }, { $set: { region: "Nairobi Metro" } })
db.schools.deleteMany({ category: "sub-county" })
```

**Query operators** start with `$`:

| SQL | MongoDB |
|---|---|
| `students > 1000` | `{ students: { $gt: 1000 } }` (`$gte`, `$lt`, `$lte`, `$ne`) |
| `county IN ('Kiambu', 'Nyeri')` | `{ county: { $in: ["Kiambu", "Nyeri"] } }` |
| `a AND b` | `{ a: ..., b: ... }` (just list both) |
| `a OR b` | `{ $or: [ {...}, {...} ] }` |
| `name LIKE 'St.%'` | `{ name: { $regex: /^St\./ } }` |
| `ORDER BY students DESC` | `.sort({ students: -1 })` |
| `LIMIT 5` | `.limit(5)` |

**Arrays are searched for you**: `{ clubs: "chess" }` matches a school whose `clubs` array *contains* `"chess"`.

**`$set` changes only the fields you name.** An update without an operator, `updateOne(filter, { region: "x" })`, is refused in mongosh; `replaceOne` replaces the whole document.

## Steps

```bash
mongosh --quiet mongodb://127.0.0.1:27018/shule < phase-7-beyond-mysql/day-083-hello-mongodb/setup.js
mongosh mongodb://127.0.0.1:27018/shule
```

Each task is a script you run the same way: `mongosh --quiet mongodb://127.0.0.1:27018/shule < starter/3-match`.

1. `starter/0-list_databases`: list the databases.
2. `starter/1-insert`: add Upendo Girls.
3. `starter/2-all`, `3-match`, `4-count`: find and count.
4. `starter/5-update`, `6-delete`.
5. `starter/7-starts_with_st`: a regular expression and a projection.
6. `pytest phase-7-beyond-mysql/day-083-hello-mongodb`

The tests run each script against a fresh copy of the schools, check what it changed with Python, and compare what it prints with the reference answer's output.

## The kata: Big Schools with Tech Clubs

In `starter/kata`, list the schools with more than 1,000 students and a chess or robotics club, names and numbers only, biggest first.

## When you're stuck

- **`DeprecationWarning: Collection.insert() is deprecated`**: older tutorials (and older exam papers) use `insert`, `update` and `count`. mongosh still runs them but warns. Use `insertOne`/`insertMany`, `updateOne`/`updateMany` and `countDocuments`. Learned MongoDB on ALX's older version? The [Phase 7 README](../README.md#coming-from-alxs-older-mongodb) lists everything that changed.
- **Nothing found, no error**: field names and values are case-sensitive, and a misspelled field silently matches nothing. `{ County: "Kiambu" }` finds no school.
- **`Stadi Technical` shows up in the St. list**: in a regular expression `.` means "any character". Escape it: `/^St\./`.
- **`Cannot do exclusion on field name in inclusion projection`**: a projection is all 1s or all 0s, except `_id`, which you can always turn off with `_id: 0`.
- **The update added `region` to every school**: the filter is the first argument; `{}` matches everything.
- **The count prints a list of schools**: `find(...)` returns the documents. `countDocuments(filter)` returns just the number.
