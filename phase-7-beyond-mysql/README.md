# Phase 7: Beyond MySQL

PostgreSQL, databases from Python, migrations, then two databases that aren't relational at all: MongoDB for documents and Redis for fast keys and caches.

**You learn:** PostgreSQL, databases from Python, SQL injection, migrations, MongoDB, document modelling, aggregation pipelines, Redis.

**It ends with:** a matatu booking system using three databases.

## The days

| Day | Project | What it teaches |
|---|---|---|
| 79 | [PostgreSQL for MySQL Users](day-079-postgresql-for-mysql-users/README.md) | psql, schemas, identity columns, the differences |
| 80 | [Postgres Superpowers](day-080-postgres-superpowers/README.md) | JSONB, arrays, full-text search |
| 81 | [Python Meets SQL](day-081-python-meets-sql/README.md) | DB-API, parameters, SQL injection |
| 82 | [Migrations](day-082-migrations/README.md) | versioned schema changes |
| 83 | [Hello, MongoDB](day-083-hello-mongodb/README.md) | the mongo shell: insert, find, update, delete |
| 84 | [MongoDB from Python](day-084-mongodb-from-python/README.md) | PyMongo |
| 85 | [Log Stats](day-085-log-stats/README.md) | aggregation pipelines |
| 86 | [Embed or Reference?](day-086-embed-or-reference/README.md) | document modelling |
| 87 | [Hello, Redis](day-087-hello-redis/README.md) | strings, keys, expiry, a Cache class |
| 88 | [Counting Calls](day-088-counting-calls/README.md) | decorators that record into Redis |
| 89 | [Caching Pages](day-089-caching-pages/README.md) | expiring caches, lists, sets, sorted sets |
| 90 | [Capstone: Matatu Bookings](day-090-capstone-matatu-bookings/README.md) | PostgreSQL, Redis and MongoDB in one app |

## How to test your work

**Run a day's tests:**

```bash
pytest phase-7-beyond-mysql/day-083-hello-mongodb                       # every test for the day
pytest phase-7-beyond-mysql/day-083-hello-mongodb -k kata               # only tests whose name contains "kata"
pytest phase-7-beyond-mysql/day-083-hello-mongodb -x --tb=short         # stop at the first failure, with a short explanation
```

Each test runs one of your files and compares the result with the right answer. A failure shows what came back and what was expected, usually as rows like `('Nakuru', '12')`. From SQL files, every value comes back as text, and `NULL` as `'NULL'`. Read the first failure only, fix it, run again.

**Many tests change the data and run your file a second time**, so an answer typed in by hand, or one that only works for today's rows, fails the second run. If the first run passes and the second fails, your query depends on something it shouldn't (an id you typed, a row's position, a name spelled out).

**Run your work by hand:**

Each database has its own prompt, and the tests use the same programs:

| Database | Open a prompt | Run a file |
|---|---|---|
| PostgreSQL | `tools/psql.sh practice` | `tools/psql.sh practice -f file.sql` |
| MongoDB | `mongosh mongodb://127.0.0.1:27018/practice` | `mongosh --quiet mongodb://127.0.0.1:27018/practice < file` |
| Redis | `redis-cli -p 6380` | (commands only) |
| Python | `PYTHONPATH=tools python -i phase-7-beyond-mysql/day-084-mongodb-from-python/starter/schools.py` | `python file.py` |

**Mongo scripts have no extension** (`starter/3-match`), the way the ALX checker names them. When you pipe one into `mongosh`, it prints a `practice>` prompt before each result. That's normal; the tests ignore it.

**Redis keys survive between runs** of your own code: `redis-cli -p 6380 flushdb` clears the course's Redis. The tests flush it before and after every test.

**Still stuck?** Read the day's "When you're stuck" section first: it lists the mistakes people actually make. Then open the same file in `solution/` and compare. It spoils the answer, so read it, close it, and write your own version from memory.

On Windows, run all of this in the Ubuntu (WSL) terminal, not PowerShell: see [WINDOWS.md](../WINDOWS.md).


## Coming from ALX's older MongoDB?

ALX's NoSQL project was written for an old MongoDB (3.6 / 4.x), the old `mongo` shell and PyMongo 3. This course uses **MongoDB 7, mongosh 2 and PyMongo 4**, and a lot of what you remember has changed name or gone:

| What ALX used | What works now | What happens if you use the old one |
|---|---|---|
| `mongo` (the shell) | `mongosh` | `mongo: command not found`: it was removed in MongoDB 6.0 |
| `mongo dbname < file` | `mongosh --quiet mongodb://127.0.0.1:27018/dbname < file` | |
| `db.schools.insert(doc)` | `insertOne(doc)` / `insertMany([...])` | still runs, with a `DeprecationWarning` |
| `db.schools.update(q, u)` | `updateOne(q, u)` / `updateMany(q, u)` | still runs, with a warning |
| `db.schools.remove(q)` | `deleteOne(q)` / `deleteMany(q)` | still runs, with a warning |
| `db.schools.count()`, `find().count()` | `countDocuments(filter)`, or `estimatedDocumentCount()` | still runs, with a warning |
| PyMongo `collection.insert(doc)` | `insert_one(doc)` / `insert_many(docs)` | **error**: PyMongo 4 removed it (`TypeError: 'Collection' object is not callable`) |
| PyMongo `update()`, `remove()`, `save()` | `update_one` / `update_many`, `delete_one` / `delete_many`, `replace_one` | **error**, the same way |
| PyMongo `count()`, `cursor.count()` | `count_documents(filter)` | **error**, the same way |
| `ObjectId("5f1d...")` in output | `ObjectId('5f1d...')`: single quotes | output that's compared character by character differs |
| `show dbs` sizes like `0.000GB` | sizes like `40.00 KiB` | |

Check what you have: `mongod --version` (7.x or 8.x), `mongosh --version` (2.x), `python -c "import pymongo; print(pymongo.version)"` (4.x). The course pins PyMongo in `requirements.txt`, so inside the course's `.venv` you always have the right one.

**If you're also doing the ALX project itself**, write the new names. If its checker still expects the old output format, that's the checker's age, not your code: the queries are the same.


## Outside the hundred days

- [The database landscape](the-database-landscape.md): a map of the databases this course doesn't teach (SQLite, SQL Server, distributed SQL, search engines, warehouses, Kafka, vectors), what each is for, and the rule for choosing. Read it after Day 90.

## Further reading

- [PostgreSQL 17 documentation](https://www.postgresql.org/docs/17/).
- [MongoDB manual](https://www.mongodb.com/docs/manual/), [mongosh](https://www.mongodb.com/docs/mongodb-shell/) and [PyMongo](https://pymongo.readthedocs.io/).
- [Redis commands](https://redis.io/docs/latest/commands/): every command, with examples to try.
