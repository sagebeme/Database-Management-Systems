# Day 63: Flexible Fields

## The brief

A duka sells phones, shoes, food and lamps. A phone has RAM and storage; shoes have a size and colour; food has a weight and maybe an expiry date. One table with a column for every detail of every kind of product would be mostly `NULL`, and it would need an `ALTER TABLE` whenever the shop starts selling something new. The normalised answer (Day 33) is a table per kind of product, which is right when the kinds are few and stable.

There's a third way, for details that really do vary: a **JSON column**. MySQL stores it as checked, binary JSON, and gives you functions to read it, change it, index it and even validate it. Today you use all of those, and see where it beats tables and where it doesn't.

## What you'll use

| You want | Write |
|---|---|
| a value, as JSON | `attributes->'$.ram_gb'` (`4`, or `"red"` with quotes) |
| a value, as plain text | `attributes->>'$.colour'` (`red`) |
| a number to compare or sort | `CAST(attributes->>'$.ram_gb' AS UNSIGNED)` |
| set or add a key | `JSON_SET(attributes, '$.on_offer', TRUE)` (also `JSON_INSERT`, `JSON_REPLACE`, `JSON_REMOVE`) |
| does a key exist? | `JSON_CONTAINS_PATH(attributes, 'one', '$.on_offer')` |
| is a value in an array? | `'new' MEMBER OF (attributes->'$.tags')` |
| an array's items as rows | `JSON_TABLE(attributes, '$.tags[*]' COLUMNS (tag VARCHAR(30) PATH '$'))` (Day 48) |
| build JSON | `JSON_OBJECT('name', name, 'price', price)`, `JSON_ARRAY(...)`, `JSON_ARRAYAGG(name)` |

- **Paths**: `$` is the whole document, `$.size` a key, `$.tags[0]` the first item of an array, and `$.tags[*]` every item.
- **`->>` gives text.** Sorting by it sorts as text (`'12'` comes before `'4'`), so `CAST` when you mean a number.
- **A missing key gives `NULL`**, not an error.
- **Generated columns** work a value out from other columns and keep it up to date by themselves:

  ```sql
  ALTER TABLE products ADD COLUMN ram_gb INT GENERATED ALWAYS AS (attributes->>'$.ram_gb') VIRTUAL;
  ```

  `VIRTUAL` is computed when read; `STORED` is saved on disk. Either can be indexed, which is **how you index inside JSON**: index the generated column. You can't write to one.
- **Validating JSON**: `JSON_SCHEMA_VALID(schema, document)` checks a document against a JSON Schema (`type`, `required`, `properties`, `minimum`, ...). It can go in a `CHECK` constraint.

**When to use JSON**: details that vary by kind and that you mostly store and show. **When not to**: anything you join on, total, or that needs a foreign key. If every row has it and queries filter on it, it deserves a real column.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS catalogue;"
tools/mysql.sh catalogue < phase-5-advanced-mysql/day-063-flexible-fields/setup.sql
```

1. `starter/0-phones.sql`: phones with at least 4 GB of RAM.
2. `starter/1-on_offer.sql`: mark the cheap products as on offer.
3. `starter/2-ram_column.sql`: a generated `ram_gb` column, indexed.
4. `starter/3-new_arrivals.sql`: products tagged `new`.
5. `starter/4-tag_counts.sql`: every tag and its count.
6. `pytest phase-5-advanced-mysql/day-063-flexible-fields`

## The kata: Check the Shape

In `starter/kata.sql`, add a `CHECK` constraint, `phone_shape`, that uses `JSON_SCHEMA_VALID` so a phone can't be saved without `ram_gb` and `storage_gb`, both whole numbers of 0 or more. Other categories stay free. Hint: `CHECK (category <> 'phone' OR JSON_SCHEMA_VALID('{...}', attributes))`.

## When you're stuck

- **`"red"` comes back with quotes**: that's `->`. Use `->>` for the plain value.
- **`ERROR 3143: Invalid JSON path expression`**: paths start with `$`, and keys with spaces need quotes: `'$."unit price"'`.
- **`ERROR 1136: Column count doesn't match value count`** after step 3: the table has a new column, so an `INSERT` without a column list no longer fits. Name the columns.
- **`ERROR 3105: The value specified for generated column 'ram_gb' ... is not allowed`**: generated columns are read-only. Change the JSON instead.
- **`on_offer` comes out as `"true"` (text)**: write `TRUE`, not `'true'`.
- **The tag counts miss products**: you need the comma (or `CROSS JOIN`) before `JSON_TABLE`, so it runs for each product's own `attributes`.
- **The kata's constraint is refused straight away**: an existing phone breaks your schema. Check the property names are spelt as in the data.
