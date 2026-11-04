# Day 15: One Table Is Not Enough

## The brief

Soma Stationers in Nakuru keeps every order in one big table. Each row has the order, the customer's name, phone and town, the item and its price. It looked simple when they started. Now the owner, Mr Kirui, has noticed odd things:

- Kamau Njoroge appears with two different phone numbers. Which is right?
- An exercise book is 60 bob in some rows and 65 in another. What does it cost?
- When Chebet's only order for manila paper is deleted, the shop will have no record that it sells manila paper at all.

These are the three classic **anomalies** of a badly designed table, and they all come from storing the same fact in many rows:

| Anomaly | What goes wrong |
|---|---|
| **Update** | A fact stored in five rows must be changed in all five. Miss one and the data contradicts itself (Kamau's phone). |
| **Insert** | You can't record a fact without an unrelated one: no adding a new item to the price list until someone orders it. |
| **Delete** | Deleting one thing deletes another: the last manila-paper order takes the item with it. |

The cure is to keep each fact **once**, in its own table: customers in one, items in another, orders pointing at them. Phase 2 is about building and querying databases made of many tables. Phase 4 turns today's instinct into rules (normalisation).

## What you'll use

All tools you already know, plus one new statement:

```sql
CREATE TABLE towns AS
SELECT DISTINCT customer_town AS name FROM orders_flat;
```

`CREATE TABLE ... AS SELECT` makes a new table from a query's result: its columns are named after the query's columns, and its rows are the query's rows. It's the quick way to pull a repeated fact out into its own table. (It doesn't copy keys or constraints; Day 16 adds those.)

To find contradictions, count the *different* values each thing has: a customer should have one phone, so `COUNT(DISTINCT customer_phone) > 1` is a problem.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS stationery;"
tools/mysql.sh stationery < phase-2-many-tables/day-015-one-table-is-not-enough/setup.sql
```

1. `starter/0-many_phones.sql`: customers with more than one phone: `customer_name`, `phones`. Alphabetical.
2. `starter/1-fix_kamau.sql`: Kamau's real number is `254720000001`; make all his rows say so. Notice how many rows one fact touches.
3. `starter/2-customers_table.sql`: create `customers` with one row per customer: columns `name`, `phone`, `town`. (The test fixes Kamau's phone first.)
4. `starter/3-price_conflicts.sql`: items recorded at more than one price: `item`, `prices`. Alphabetical.
5. `starter/4-items_table.sql`: create `items` with one row per item: `name`, and `price` as the highest price recorded.
6. `pytest phase-2-many-tables/day-015-one-table-is-not-enough`

## The kata: Lost With the Order

In `starter/kata.sql`, list the items that appear in only one order, with that order's id: `item`, `order_id`. Alphabetical. Deleting any of those orders would make the shop forget the item.

## When you're stuck

- **The customers table has four rows**: Kamau still has two phones there. In the test the fix runs first; at your prompt, run step 2 before step 3.
- **`items` has two rows for exercise books**: `DISTINCT item, item_price` keeps both prices. Group by the item and pick one price with `MAX`.
- **`ERROR 1050: Table 'customers' already exists`**: drop it (`DROP TABLE customers;`) before running the file again at your prompt.
- **The kata needs the order id, but grouping hides it**: when a group has exactly one row, `MIN(order_id)` (or `MAX`) *is* that row's id.
