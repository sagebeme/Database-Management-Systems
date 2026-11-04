# Syllabus

One hundred days, eight phases, from your first `SELECT` to designing, tuning and running databases like a senior engineer. Each phase ends with a capstone that uses everything before it. The Status column says which days are written (**Done**) and which are still **Planned**.

Every day has two parts:

- **The project**: a small job with a story, a `starter/` folder where you write your answers, and tests that run them against a real database.
- **The kata**: a 5–15 minute puzzle at the end, in the style of HackerRank's SQL questions or GATE's database questions, tested the same way.

Where the topics come from: the SQL and NoSQL projects of the ALX software engineering programme (`0x0D` SQL introduction, `0x0E` more queries, `0x00` MySQL advanced, `0x01` NoSQL, `0x02` Redis basics), and the whole GATE CSE databases syllabus (ER model, relational algebra and calculus, SQL, functional dependencies and normalisation, transactions and concurrency, file structures and B+ trees).

## Phase 1: SQL from zero

Learn: databases and tables, data types, inserting, selecting, filtering, sorting, aggregates, grouping, NULL, functions, character sets
Ends with: a weather report for Kenya's counties

| Day | Project | What it teaches | Status |
|---|---|---|---|
| 1 | Hello, MySQL | the server, SHOW, CREATE and DROP DATABASE, idempotent scripts | Done |
| 2 | The Chama Register | CREATE TABLE, data types, SHOW TABLES, DESCRIBE | Done |
| 3 | Sukuma Prices | INSERT, SELECT, SHOW CREATE TABLE | Done |
| 4 | Matatu Stages | WHERE, comparison operators, IS NULL | Done |
| 5 | M-Pesa Search | AND, OR, NOT, IN, BETWEEN, LIKE | Done |
| 6 | KCSE Top Ten | ORDER BY, LIMIT, OFFSET, DISTINCT | Done |
| 7 | Fixing the Register | UPDATE and DELETE, safely | Done |
| 8 | Shop Totals | COUNT, SUM, AVG, MIN, MAX | Done |
| 9 | Sales by Category | GROUP BY | Done |
| 10 | Best-Selling Saccos | HAVING, and the order SQL runs a query in | Done |
| 11 | Missing Phone Numbers | NULL, three-valued logic, COALESCE | Done |
| 12 | Receipts and Due Dates | string, number and date functions, CASE | Done |
| 13 | Majina na Emoji | character sets, utf8mb4, collations | Done |
| 14 | Capstone: County Weather Report | everything in Phase 1 on one dataset | Done |

## Phase 2: Many tables

Learn: keys and constraints, foreign keys, subqueries, joins of every kind, many-to-many, changing tables, users and privileges, views, importing data
Ends with: a report on Riverwood, a Kenyan film and TV database

| Day | Project | What it teaches | Status |
|---|---|---|---|
| 15 | One Table Is Not Enough | repeated data and the trouble it causes | Done |
| 16 | Rules for Rows | PRIMARY KEY, AUTO_INCREMENT, UNIQUE, NOT NULL, DEFAULT | Done |
| 17 | Counties and Towns | FOREIGN KEY, ON DELETE | Done |
| 18 | Towns in Nakuru | subqueries | Done |
| 19 | Town, County | INNER JOIN | Done |
| 20 | Every Town, Even Alone | LEFT, RIGHT and full outer joins | Done |
| 21 | Riverwood: Shows and Genres | many-to-many and junction tables | Done |
| 22 | Not a Comedy | anti-joins, NOT IN, NOT EXISTS | Done |
| 23 | Ratings | joins with aggregates | Done |
| 24 | Changing the Shape | ALTER TABLE, DROP, TRUNCATE vs DELETE | Done |
| 25 | Who Can See What | users, GRANT, REVOKE | Done |
| 26 | Views | CREATE VIEW, updatable views | Done |
| 27 | Loading Real Data | importing CSV, LOAD DATA | Done |
| 28 | Capstone: The Riverwood Report | twelve questions about a TV database | Done |

## Phase 3: Designing databases

Learn: why a DBMS beats files, keys, integrity constraints, ER diagrams, cardinality, weak entities, the relational model, relational algebra, tuple and domain relational calculus
Ends with: a hospital database designed from a brief

| Day | Project | What it teaches | Status |
|---|---|---|---|
| 29 | The Exercise Book Problem | files vs a DBMS, built in Python | Done |
| 30 | Which Column Is the Key? | super, candidate, primary, alternate and foreign keys | Done |
| 31 | Rules the Database Enforces | domain, entity and referential integrity | Done |
| 32 | Drawing the Shop | ER diagrams: entities, attributes, relationships | Done |
| 33 | One, Many, Many-to-Many | cardinality, participation, the fewest tables | Done |
| 34 | Dependants and Managers | weak entities, self-referential relationships | Done |
| 35 | Tables Are Sets | the relational model in maths | Done |
| 36 | Relational Algebra I | select, project, rename, union, difference, product | Done |
| 37 | Relational Algebra II | joins and division | Done |
| 38 | Relational Calculus | tuple and domain calculus, safe queries | Done |
| 39 | Practice Test 1 | GATE-style questions on Phases 1–3 | Done |
| 40 | Capstone: Design a Hospital | from a brief to an ER diagram, tables and queries | Done |

## Phase 4: Normalisation

Learn: anomalies, functional dependencies, attribute closure, candidate keys, Armstrong's axioms, minimal covers, lossless and dependency-preserving decomposition, 1NF to 4NF
Ends with: an M-Pesa agent's spreadsheet turned into a clean schema

| Day | Project | What it teaches | Status |
|---|---|---|---|
| 41 | The Messy Spreadsheet | insert, update and delete anomalies | Planned |
| 42 | Does It Depend? | functional dependencies, checked against data | Planned |
| 43 | Closure | attribute closure and finding every candidate key | Planned |
| 44 | Same Rules, Different Words | Armstrong's axioms, implied and equivalent FD sets | Planned |
| 45 | The Shortest Rulebook | minimal and canonical covers | Planned |
| 46 | Splitting Without Losing | lossless-join decomposition | Planned |
| 47 | Splitting Without Forgetting | dependency-preserving decomposition | Planned |
| 48 | First and Second Normal Form | atomic values, partial dependencies | Planned |
| 49 | Third Normal Form and BCNF | transitive dependencies, 3NF synthesis, BCNF decomposition | Planned |
| 50 | Fourth Normal Form | multi-valued dependencies | Planned |
| 51 | Breaking the Rules on Purpose | denormalisation, summary tables | Planned |
| 52 | Capstone: The Agent's Ledger | normalise a real-looking spreadsheet and migrate the data | Planned |

## Phase 5: Advanced MySQL

Learn: CHECK and ENUM, window functions, CTEs, recursive queries, triggers, stored procedures and functions, indexes, JSON
Ends with: a school results system that keeps itself up to date

| Day | Project | What it teaches | Status |
|---|---|---|---|
| 53 | Unique Users | constraints in depth: CHECK, ENUM, UNIQUE | Planned |
| 54 | Fans by Country | ranking with window functions | Planned |
| 55 | Running Totals | SUM OVER, LAG, LEAD, moving averages | Planned |
| 56 | Who Reports to Whom | CTEs and recursive CTEs | Planned |
| 57 | Band Lifespans | date arithmetic | Planned |
| 58 | Stock Goes Down | triggers I | Planned |
| 59 | Email Changed | triggers II: BEFORE UPDATE | Planned |
| 60 | Add a Bonus | stored procedures | Planned |
| 61 | Average Scores | procedures, functions, cursors | Planned |
| 62 | Finding Names Fast | CREATE INDEX, prefix indexes, EXPLAIN | Planned |
| 63 | Flexible Fields | JSON columns, generated columns | Planned |
| 64 | Capstone: Results Day | triggers, procedures, views and indexes together | Planned |

## Phase 6: Transactions and storage

Learn: ACID, isolation levels, schedules, recoverability, conflict and view serializability, locking, timestamps, deadlocks, recovery, file organisation, B-trees and B+ trees, index design
Ends with: a tiny storage engine with a B+ tree index and a log

| Day | Project | What it teaches | Status |
|---|---|---|---|
| 65 | Send Money | transactions, COMMIT, ROLLBACK, ACID | Planned |
| 66 | Two Tellers, One Account | lost updates, dirty and non-repeatable reads, phantoms | Planned |
| 67 | Isolation Levels | what each level allows, in MySQL and PostgreSQL | Planned |
| 68 | Can We Undo It? | schedules, recoverable, cascadeless and strict | Planned |
| 69 | As If One at a Time | conflict serializability, precedence graphs | Planned |
| 70 | View Serializability | view equivalence, blind writes | Planned |
| 71 | Locks | two-phase locking, SELECT ... FOR UPDATE, deadlocks | Planned |
| 72 | Timestamps | timestamp ordering, Thomas write rule, wait-die and wound-wait | Planned |
| 73 | After the Crash | write-ahead logging, undo, redo, checkpoints | Planned |
| 74 | Blocks and Records | file organisation, blocking factor, index sizes | Planned |
| 75 | B-Trees | search and insert in a B-tree | Planned |
| 76 | B+ Trees | order, insert, split, range scans | Planned |
| 77 | Indexes in Real Life | clustered and secondary indexes, composite and covering indexes | Planned |
| 78 | Capstone: Build a Storage Engine | a heap file, a B+ tree index and a log, in Python | Planned |

## Phase 7: Beyond MySQL

Learn: PostgreSQL, databases from Python, SQL injection, migrations, MongoDB, document modelling, aggregation pipelines, Redis
Ends with: a matatu booking system using three databases

| Day | Project | What it teaches | Status |
|---|---|---|---|
| 79 | PostgreSQL for MySQL Users | psql, schemas, identity columns, the differences | Planned |
| 80 | Postgres Superpowers | JSONB, arrays, full-text search | Planned |
| 81 | Python Meets SQL | DB-API, parameters, SQL injection | Planned |
| 82 | Migrations | versioned schema changes | Planned |
| 83 | Hello, MongoDB | the mongo shell: insert, find, update, delete | Planned |
| 84 | MongoDB from Python | PyMongo | Planned |
| 85 | Log Stats | aggregation pipelines | Planned |
| 86 | Embed or Reference? | document modelling | Planned |
| 87 | Hello, Redis | strings, keys, expiry, a Cache class | Planned |
| 88 | Counting Calls | decorators that record into Redis | Planned |
| 89 | Caching Pages | expiring caches, lists, sets, sorted sets | Planned |
| 90 | Capstone: Matatu Bookings | PostgreSQL, Redis and MongoDB in one app | Planned |

## Phase 8: Expert

Learn: query plans and join algorithms, partitioning and sharding, replication and backups, security, data warehousing
Ends with: a production-ready database for a real business, designed and defended

| Day | Project | What it teaches | Status |
|---|---|---|---|
| 91 | Reading Query Plans | EXPLAIN ANALYZE, join algorithms, cost | Planned |
| 92 | Too Big for One Table | partitioning and sharding | Planned |
| 93 | Never Lose Data | backups, restores, replication | Planned |
| 94 | Lock It Down | least privilege, row-level security, auditing | Planned |
| 95 | The Data Warehouse | star schemas, OLTP vs OLAP, ETL | Planned |
| 96 | Portfolio: SACCO Database | a brief and its tests, no walkthrough | Planned |
| 97 | Portfolio: The SQL Interview | twenty hard questions, HackerRank-style | Planned |
| 98 | Portfolio: Build a Key-Value Store | a log-structured store with compaction | Planned |
| 99 | The Final Exam | a full GATE-style subject test | Planned |
| 100 | Capstone: Your Own Production Database | design doc, schema, migrations, queries, indexes and tests | Planned |
