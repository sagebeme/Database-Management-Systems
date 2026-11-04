# Day 17: Counties and Towns

## The brief

A logistics startup in Nairobi is building its delivery map, starting with Kenya's counties and the towns in each. Day 15 taught you to keep each fact once: counties in one table, towns in another. But then a town needs to say *which* county it's in, and the database should make sure that county really exists. No town in county 99, and no deleting Nakuru while Naivasha still points at it.

That link is a **foreign key**: a column in one table whose values must match the primary key of another.

```
counties                         towns
+----+------+---------+          +----+-----------+----------+
| id | code | name    |          | id | county_id | name     |
+----+------+---------+          +----+-----------+----------+
|  5 | 032  | Nakuru  | <------- |  9 |         5 | Nakuru   |
|    |      |         | <------- | 10 |         5 | Naivasha |
+----+------+---------+          +----+-----------+----------+
```

`data.sql` fills both tables with seven real counties (with their official codes) and thirteen real towns. It only inserts rows, so it works only once your tables are right.

## What you'll use

```sql
CREATE TABLE IF NOT EXISTS towns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    county_id INT NOT NULL,
    name VARCHAR(60) NOT NULL,
    FOREIGN KEY (county_id) REFERENCES counties (id)
);
```

- The **parent** (`counties`) must exist first, and the column it points at must be a key.
- **Inserting** a town whose `county_id` isn't in `counties` fails: `Cannot add or update a child row: a foreign key constraint fails`.
- **Deleting** a county that towns still point at fails too. You choose what should happen instead with `ON DELETE`:

| `ON DELETE ...` | When the parent row is deleted |
|---|---|
| (nothing) / `RESTRICT` | refuse |
| `CASCADE` | delete the children too |
| `SET NULL` | set the children's column to `NULL` (it must allow `NULL`) |

  `CASCADE` is right when the children make no sense alone (a town's wards); `RESTRICT` is right when deleting by accident would be a disaster (a county with towns).

- **Look ids up instead of typing them.** `INSERT ... SELECT` inserts the rows a query returns:

  ```sql
  INSERT INTO towns (county_id, name)
  SELECT id, 'Gilgil' FROM counties WHERE name = 'Nakuru';
  ```

  If Nakuru's id ever changes, this still works.

- `information_schema.key_column_usage` lists key columns; for a foreign key, `referenced_table_name` says which table it points at.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS places;"
```

1. `starter/0-counties_table.sql`: `counties`: `id` (auto-numbered primary key), `code` (`CHAR(3)`, required, unique), `name` (`VARCHAR(60)`, required, unique).
2. `starter/1-towns_table.sql`: `towns`: `id` (auto-numbered primary key), `county_id` (required, must be a real county), `name` (`VARCHAR(60)`, required).
3. Load the data: `tools/mysql.sh places < phase-2-many-tables/day-017-counties-and-towns/data.sql`
4. `starter/2-add_gilgil.sql`: add Gilgil to Nakuru, looking up Nakuru's id by name in the same statement.
5. `starter/3-wards_table.sql`: `wards`: `id` (auto-numbered primary key), `town_id` (required, a real town), `name` (`VARCHAR(60)`, required). Deleting a town deletes its wards.
6. `starter/4-delete_kisumu.sql`: Kisumu (id 6) is leaving the list: delete it and its towns. Mind the order.
7. `pytest phase-2-many-tables/day-017-counties-and-towns`

## The kata: Who Points Here?

In `starter/kata.sql`, list every table and column in the current database with a foreign key to `counties`: `table_name`, `column_name`, alphabetical. (Before you drop a table, this tells you what depends on it.)

## When you're stuck

- **`ERROR 1824: Failed to open the referenced table 'counties'`**: create `counties` before `towns`.
- **`ERROR 3780: Referencing column 'county_id' and referenced column 'id' ... are incompatible`**: both must be the same type (`INT` and `INT`).
- **`data.sql` fails with `Unknown column`**: compare your column names with the ones above.
- **Deleting Kisumu fails with `a foreign key constraint fails`**: delete its towns first, then the county.
- **The Gilgil test fails after Nakuru's id changes**: you typed `5`. Use `INSERT ... SELECT ... WHERE name = 'Nakuru'`.
