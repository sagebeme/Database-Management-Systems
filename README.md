# Database Management Systems: 100 Days

From your very first `SELECT` to designing, tuning and running databases like a senior engineer, one small job a day. Every day has a story, a starter for you to fill in, and tests that run your answers against a **real database** and tell you when they're right.

No experience needed. If you can open a terminal and edit a text file, you can start Day 1.

## What you'll be able to do

- Write SQL fluently: filtering, grouping, every kind of join, subqueries, window functions, recursive queries.
- Design a database from a business brief: ER diagrams, keys, constraints, and normalisation up to BCNF and 4NF.
- Explain and use transactions, isolation levels and locks, and know what really happens when two people update the same row.
- Know how a database stores data on disk: pages, B+ trees, indexes and logs, and how to make a slow query fast.
- Use PostgreSQL, MongoDB and Redis as well as MySQL, and choose between them.
- Pass the databases section of GATE CSE, and the SQL rounds of a technical interview.

The topics cover the full GATE CSE databases syllabus and the SQL and NoSQL projects of the ALX software engineering programme. [SYLLABUS.md](SYLLABUS.md) lists all hundred days.

## The eight phases

| Phase | Days | You learn | It ends with |
|---|---|---|---|
| 1. SQL from zero | 1–14 | tables, types, `SELECT`, `WHERE`, sorting, aggregates, `GROUP BY`, `HAVING`, `NULL`, functions, character sets | a weather report for eight counties |
| 2. Many tables | 15–28 | keys, foreign keys, subqueries, joins, many-to-many, `ALTER`, users and privileges, views, imports | a report on a Kenyan film database |
| 3. Designing databases | 29–40 | files vs a DBMS, keys, integrity, ER diagrams, the relational model, relational algebra and calculus | a hospital database designed from a brief |
| 4. Normalisation | 41–52 | functional dependencies, closure, covers, decomposition, 1NF to 4NF | a messy spreadsheet turned into a clean schema |
| 5. Advanced MySQL | 53–64 | window functions, CTEs, triggers, stored procedures, indexes, JSON | a school results system |
| 6. Transactions and storage | 65–78 | ACID, isolation, serializability, locking, recovery, B+ trees, index design | a tiny storage engine of your own |
| 7. Beyond MySQL | 79–90 | PostgreSQL, Python and SQL, migrations, MongoDB, Redis | a booking system using three databases |
| 8. Expert | 91–100 | query plans, partitioning, replication, security, warehousing, portfolio projects | your own production database, designed and defended |

## How each day works

```
phase-1-first-queries/day-004-matatu-stages/
├── README.md       the brief, what you'll use, steps, the kata, and help when you're stuck
├── setup.sql       the tables and rows the day starts from (some days)
├── starter/        YOUR files: one per task, with the task written at the top
├── solution/       one way to do it, for when you're really stuck
└── test_day.py     the tests
```

1. Read the README.
2. Load the day's data, if it has a `setup.sql`.
3. Write each answer in `starter/`.
4. Run the tests until they all pass.
5. Do the kata: a 5–15 minute puzzle at the end, in the style of HackerRank's SQL questions or a GATE exam question.

The tests run your files exactly the way you'd run them yourself (`mysql my_db < 3-something.sql`), in a fresh, empty database each time, and compare what comes back with the right answer. Many tests also change the data and run your query again, so an answer typed in by hand won't pass.

Open `solution/` only after you've tried. Read it, close it, and write your own version from memory.

## Setting up

You need **Python 3.11+** and the database programs. Days 1–64 only need MySQL; PostgreSQL, MongoDB and Redis join in Phase 7.

**Ubuntu / Debian / WSL on Windows**

```bash
sudo apt install python3-venv mysql-server mysql-client postgresql redis-server
# MongoDB (Phase 7): see https://www.mongodb.com/docs/manual/administration/install-on-linux/
```

**macOS** (with Homebrew)

```bash
brew install python mysql postgresql@17 redis mongodb/brew/mongodb-community mongosh
```

Then, from this folder:

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
tools/devdb.sh up          # start your own private MySQL, PostgreSQL, MongoDB and Redis
pytest phase-1-first-queries/day-001-hello-mysql
```

`tools/devdb.sh up` starts copies of each database that belong to you: no `sudo`, no passwords, and nothing touches a database server you already run. They listen on `127.0.0.1` on their own ports (MySQL 3307, PostgreSQL 5434, MongoDB 27018, Redis 6380). `tools/devdb.sh status` shows what's running; `tools/devdb.sh down` stops them. On Ubuntu, the private MySQL keeps its data under `/tmp` (Ubuntu's AppArmor rules only let MySQL write there), so it starts empty after a reboot. That's fine: every day loads its own data.

**Using your own servers instead?** Copy `.env.example` to `.env` and fill in the host, port, user and password. The tests and `tools/mysql.sh` read it. `.env` is ignored by Git; never commit real passwords.

**Opening a prompt**

```bash
tools/mysql.sh                                   # mysql> prompt
tools/mysql.sh duka < path/to/setup.sql          # run a file inside the database duka
tools/psql.sh                                    # postgres=# prompt (Phase 7)
```

## Checking the whole course

```bash
python tools/verify.py         # every day: the solution passes, the untouched starter fails
python tools/verify.py 3 14    # just Days 3 and 14
```

GitHub Actions runs the same check on every push (`.github/workflows/ci.yml`).

## Where the material comes from

- The **GATE CSE databases syllabus**: ER and relational models, relational algebra, tuple and domain calculus, SQL, functional dependencies and normalisation, transactions and concurrency control, file organisation, indexing and B+ trees.
- The **ALX software engineering programme**'s database projects: SQL introduction and more queries (Phases 1–2), MySQL advanced (Phase 5), NoSQL with MongoDB, and Redis basics (Phase 7).

Every dataset is made up for practice unless its `setup.sql` says otherwise, and each one says which parts are real (place names, for example) and which are invented.
