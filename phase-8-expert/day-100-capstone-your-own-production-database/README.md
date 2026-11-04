# Day 100: Capstone: Your Own Production Database

## The brief

The last day is yours. Pick a real problem, ideally one someone you know actually has: a chama's contributions, a church's tithes and pledges, a boda stage's daily dues, a clinic's appointments, a school's fees, a shop's credit book. Then build the database for it the way a professional would, from the design doc to the restore plan.

`solution/` holds a worked example, **Shule Fees** (a school's M-Pesa fee payments). Read it *after* you've written your own design doc, not before: it's one answer, not the answer.

The tests don't know what your project is about. They check that it's built like a production database:

| The tests check | Course days |
|---|---|
| `DESIGN.md` has a Problem, Data model, Access patterns, Indexes, Backups and recovery, and Security section, at least 300 words, no `TODO`s | all of it |
| its Mermaid ER diagram has at least 4 entities with their attributes and primary keys, and 3 relationships | 32–34 |
| the diagram's entities and attributes are exactly your tables and columns | 32–40 |
| the schema is built by at least three migrations in `migrations/`, run in order | 82 |
| every table has a primary key; at least 3 foreign keys, 3 `CHECK`s and 1 `UNIQUE`; every foreign key is indexed | 30, 31, 53, 77 |
| `seed.sql` fills every table, one with at least 10,000 rows | 27, 92 |
| at least five queries in `queries/`, each starting `-- question:`, each returning rows | 1–28, 54–56 |
| none of them reads a whole 10,000-row table, unless it says why with `-- full scan:` | 62, 77, 91 |
| at least five statements in `checks.sql` that the database refuses | 31, 53 |
| `security.sql` creates a `capstone_app` role that can log in and read, owns nothing, and can't truncate or drop | 25, 94 |

## What you'll use

Everything. In particular:

- **Design before SQL.** Write `DESIGN.md` first: the problem, the access patterns (the questions people will ask, and how often), then the tables that answer them. Normalise (Phase 4), then denormalise only where an access pattern needs it (Day 51), and say so.
- **Migrations, not a schema file** (Day 82). Production databases are never rebuilt; they're changed one step at a time. Split your schema the way it would really have grown.
- **Let the database say no** (Days 31, 53). Every rule you can write as a constraint, write as a constraint. `checks.sql` proves they work: each statement after a `-- expect error:` line must fail.
- **Indexes for questions** (Days 62, 77, 91). An index exists to answer an access pattern. A report that reads half the table should scan it; say so with `-- full scan: <why>`.
- **Least privilege** (Day 94). The app never connects as the owner.

## Steps

1. Choose the problem. Talk to the person who has it if you can.
2. Write `starter/DESIGN.md`, the diagram included. Run `pytest phase-8-expert/day-100-capstone-your-own-production-database -k design` until it passes.
3. Write the migrations, then `-k "migrations or diagram or constraints"`.
4. Write `seed.sql` with `generate_series` (Day 92), then the queries, then `checks.sql` and `security.sql`.
5. `pytest phase-8-expert/day-100-capstone-your-own-production-database`
6. Copy `starter/` into a repository of its own, with a README that links the design doc and shows one query plan. That's the project you talk about in interviews.

You can add more files than the starter has (more migrations, more queries); the tests read them all. Keep the names: migrations are `NNN.sql`, run in name order.

## The kata: Undo It

A migration that can't be undone is a one-way door at 2 a.m. In `starter/migrations/down/`, write the file that undoes your **last** migration (the same name as it): after it runs, the schema must be exactly what it was before that migration, and the migration must apply again cleanly.

## When you're stuck

- **The diagram and the database disagree**: entity names must be the table names (lower case is safest) and attributes the column names. Mermaid types are free text; `int`, `string`, `date` are fine.
- **"Index every foreign key"**: `CREATE INDEX ON child (parent_id)`. A composite foreign key needs an index whose leading columns are exactly its columns. A `UNIQUE` or primary key that starts with them counts.
- **A query scans a big table you thought was indexed**: run `EXPLAIN` on it (Day 91). A function on the column (`date(paid_at) = ...`) hides the index; compare with a range instead. Run `ANALYZE` after seeding.
- **A check isn't refused**: the rule lives only in your head or your app. Make it a constraint.
- **`role "capstone_app" already exists`**: roles belong to the whole server. `DROP ROLE capstone_app;` after dropping your scratch database.
- **Stuck choosing a project**: do Shule Fees in your own way, then change one big thing (fee waivers, siblings sharing a guardian, a bursary paying part).
