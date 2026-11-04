# Day 85: Log Stats

## The brief

Monday morning, and the matatu booking API had a rough weekend. The team lead wants answers: how many requests, which methods, which IPs hammered us, what hour was busiest, which endpoints are throwing errors, and which are slow. The answers are in the web server's logs, 600 of them, in MongoDB.

You could pull every document into Python and count with loops. With a million logs that means shipping a million documents over the network to throw most of them away. An **aggregation pipeline** does the counting inside the database and sends back only the answer: MongoDB's version of `GROUP BY`.

## What you'll use

A pipeline is a list of **stages**; documents flow through them in order:

```python
nginx.aggregate([
    {"$match": {"status": {"$gte": 500}}},                          # WHERE
    {"$group": {"_id": "$path", "errors": {"$sum": 1}}},            # GROUP BY path, COUNT(*)
    {"$sort": {"errors": -1, "_id": 1}},                            # ORDER BY errors DESC, path
    {"$limit": 10},                                                 # LIMIT 10
])
```

| SQL | stage |
|---|---|
| `WHERE` | `$match` (put it first: it can use indexes and shrinks everything after it) |
| `GROUP BY x` + aggregates | `$group` with `_id: "$x"` and `$sum`, `$avg`, `$min`, `$max`, `$push` |
| `SELECT` expressions | `$project`, `$addFields` |
| `HAVING` | a `$match` after the `$group` |
| `ORDER BY`, `LIMIT` | `$sort`, `$limit`, `$skip` |
| a join | `$lookup` (Day 86) |
| one row per array element | `$unwind` |

`"$path"` with a dollar means "the value of the field `path`". `{"$sum": 1}` adds 1 per document, a count. `{"$hour": "$at"}` takes the hour from a date. `{"$avg": "$topics.score"}` in a `$project` averages an array of numbers inside one document.

`count_documents(filter)` is fine for one count. For counts *per* something, group.

**Sorting and missing values**: in MongoDB's order, `null` comes before every number, so a descending sort puts students with no average last.

## Steps

Load the logs into your own MongoDB:

```bash
python phase-7-beyond-mysql/day-085-log-stats/logs_data.py
mongosh mongodb://127.0.0.1:27018/logs
```

and look: `db.nginx.findOne()`, `db.nginx.countDocuments()`. Then:

1. `starter/log_stats.py`: `report` (with `count_documents`; the format must match exactly, tabs and all), `top_ips`, `per_hour`, `errors_by_path`, `slowest_paths`.
2. `pytest phase-7-beyond-mysql/day-085-log-stats`

The tests add a few odd logs (a `HEAD` request, a new path, a request just after midnight) and check your answers against counts worked out in Python.

## The kata: Top Students

The school from Days 83 and 84 keeps each student's topics and scores inside the student's document. In `starter/log_stats.py`, write `top_students(students)`: every student with their average score, best first, in one pipeline.

## When you're stuck

- **`report` is out by a line or a tab**: copy the format from the docstring. Each method line starts with a tab character (`\t`), not spaces.
- **The status check counts 51 after the extra logs**: it counts `GET` requests to `/status` only.
- **`$group` says `a group specification must include an _id`**: every group needs `_id`, the thing you group by (`None` for one group of everything).
- **Ties come out in a different order**: sort on two fields, `{"requests": -1, "_id": 1}`. A dict keeps its order in Python 3.7 and later, so the first key sorts first.
- **`slowest_paths` gives 966.6299...**: round in Python with `round(x, 1)`, or with `$round` in the pipeline.
- **The kata: Halima's average is `None`**: `$avg` of an empty array is `null`, and that's expected. Sort descending and she comes last.
