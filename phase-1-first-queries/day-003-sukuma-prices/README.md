# Day 3: Sukuma Prices

## The brief

Mama Wanjiru's database exists, and now it needs something in it. Her price list goes into a table called `produce`, one row per item. Customers phone in orders, and those need a table too.

`setup.sql` creates `produce` with four items:

```
+----+----------+-------+-----------+
| id | name     | unit  | price_kes |
+----+----------+-------+-----------+
|  1 | Tomatoes | kg    |    120.00 |
|  2 | Onions   | kg    |     90.00 |
|  3 | Managu   | bunch |     30.00 |
|  4 | Avocado  | piece |     15.00 |
+----+----------+-------+-----------+
```

Today you read it, add to it, and make an `orders` table with these four orders:

| customer | item | qty |
|---|---|---|
| Kamau | Tomatoes | 2 |
| Njeri | Managu | 3 |
| Otieno | Avocado | 6 |
| Njeri | Onions | 1 |

## What you'll use

```sql
INSERT INTO produce (id, name, unit, price_kes) VALUES (6, 'Dhania', 'bunch', 10.00);

INSERT INTO produce (id, name, unit, price_kes) VALUES   -- many rows at once
    (7, 'Carrots', 'kg', 80.00),
    (8, 'Kales', 'bunch', 20.00);

SELECT * FROM produce;               -- every column
SELECT name, price_kes FROM produce; -- just these two, in this order
SELECT name, price_kes * 2 AS double_price FROM produce;   -- work something out
SHOW CREATE TABLE produce;           -- the CREATE statement for a table that exists
```

- **Text goes in single quotes**: `'Sukuma wiki'`. Numbers don't.
- **Name the columns** in an `INSERT`. Without the list, the values must match every column in table order, and the statement breaks the day someone adds a column.
- **`AS` names a result column.** A name with spaces or other odd characters needs backticks: `` AS `price for 3` ``. Backticks quote *names* (tables, columns); single quotes quote *text*. Mixing them up is the most common SQL typo there is.
- `SELECT *` is handy at the prompt, but in real code list the columns you need: it's clearer, and it doesn't change when the table does.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS mama_mboga;"
tools/mysql.sh mama_mboga < phase-1-first-queries/day-003-sukuma-prices/setup.sql
```

1. `starter/0-full_table.sql`: show the statement that would create `produce`.
2. `starter/1-list_values.sql`: list every row and column of `produce`.
3. `starter/2-insert_value.sql`: add Sukuma wiki: id `5`, unit `bunch`, price `20.00`.
4. `starter/3-full_creation.sql`: create `orders` (`customer VARCHAR(50)`, `item VARCHAR(50)`, `qty INT`) if it doesn't exist, then insert the four orders above. One file, two statements.
5. `starter/4-two_columns.sql`: list only `name` and `price_kes`.
6. `pytest phase-1-first-queries/day-003-sukuma-prices`

Run `setup.sql` again whenever you want the original four rows back: it drops and recreates the table.

## The kata: Price for Three

In `starter/kata.sql`, list every item's `name`, and the price of three of it in a column called `price for 3` (with the spaces).

## When you're stuck

- **`ERROR 1054: Unknown column 'Sukuma wiki' in 'field list'`**: you used backticks or double quotes around text. Text takes single quotes.
- **`ERROR 1136: Column count doesn't match value count`**: the number of values isn't the number of columns you listed.
- **`ERROR 1064 ... near 'for 3'`**: a name with spaces needs backticks.
- **Sukuma is in twice**: you ran the insert twice. Run `setup.sql` to start again.
- **The orders test fails on the second run**: `CREATE TABLE IF NOT EXISTS`.
