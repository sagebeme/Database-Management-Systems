# Day 82: Migrations

## The brief

The matatu sacco's fleet app is live. Its database has real vehicles in it, and the app keeps changing: this week it needs seat counts, next week owners in their own table. You can't drop the database and run a fresh `setup.sql` any more. And the change has to happen the same way on your laptop, your teammate's, the test server and production, in the same order, exactly once each.

That's what **migrations** are: numbered files of schema changes, kept in git with the code, and a small program that runs whichever ones a database hasn't had yet. Every framework has one (Django, Rails, Alembic, Flyway, Prisma, golang-migrate). Today you'll write one, and the migrations it runs, including one that moves live data.

## What you'll use

```
migrations/
  001_create_vehicles.sql
  002_add_seats.sql
  003_owners_table.sql
```

The database remembers what it has had:

```
schema_migrations
 version | name            | checksum   | applied_at
       1 | create_vehicles | 3f9a...    | 2026-03-02 09:14
       2 | add_seats       | b71c...    | 2026-03-09 16:40
```

**The rules** every migration tool follows:

1. **Run in order, once each.** Compare the files with `schema_migrations` and run only the missing ones.
2. **One transaction per migration**, holding both the change and its row in `schema_migrations`. If the migration fails, neither happens and the database is exactly as it was before that file. This works because Postgres DDL is transactional (Day 79). In MySQL, `CREATE` and `ALTER` commit immediately, so a half-applied migration is possible and has to be cleaned up by hand.
3. **Never edit a migration that has run.** Other databases already have the old version, and they'll never see your edit. Add a new migration instead. Storing a checksum of each file catches people who forget.
4. **Changes must work on a database with data in it.** Adding a `NOT NULL` column needs a `DEFAULT` for the rows already there. Splitting a column means creating the new table, copying the data across, pointing the old rows at the new ones, and only then dropping the old column.

**psycopg runs a whole file in one call**: `cur.execute(text)` accepts several statements separated by `;` when you pass no parameters.

**Useful string functions for 003**: `split_part('Wanjiku Kamau (254711000001)', ' (', 1)` is `Wanjiku Kamau`; `split_part(..., ' (', 2)` is `254711000001)`, and `rtrim(..., ')')` takes off the bracket. `UPDATE vehicles AS v SET ... FROM owners AS o WHERE ...` updates with a join.

## Steps

1. Write the three migrations in `starter/migrations/`. Each file says what it must do. Try each one by hand with `tools/psql.sh`, with some vehicles inserted between 001 and 002.
2. `starter/migrate.py`: `migration_files`, `applied` and `migrate`. `MigrationError` and `checksum` are done.
3. `pytest phase-7-beyond-mysql/day-082-migrations`

The tests run your migrations with `psql` on a fleet with four vehicles, and run your runner on migrations they make up, including one that fails half-way.

## The kata: Who Edited History?

In `starter/migrate.py`, write `check_history(conn, folder)`: raise `MigrationError` if a migration that has run has since been edited (its checksum changed) or deleted. `migrate` calls it before applying anything. Until you write it, it does nothing.

## When you're stuck

- **`column "seats" of relation "vehicles" contains null values`**: a new `NOT NULL` column needs a `DEFAULT` in the same `ADD COLUMN`.
- **003: `column "owner_id" of relation "vehicles" contains null values`**: add `owner_id` allowing `NULL`, fill it with an `UPDATE`, *then* `SET NOT NULL`.
- **003: Wanjiku Kamau appears twice in owners**: `SELECT DISTINCT`, one row per phone.
- **003 numbers the owners in the wrong order**: an identity column numbers rows in the order they're inserted. `ORDER BY` the phone in the `INSERT ... SELECT`.
- **After a failed migration, the table it created is still there**: run the migration *and* its `schema_migrations` row inside one `with conn.transaction():`.
- **The failure test says 003 ran**: stop at the first failure. Raise `MigrationError` from the `except`, naming the file.
- **`can't execute an empty query`**: a migration file with only comments in it. Write the migration.
