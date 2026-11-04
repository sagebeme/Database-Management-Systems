# Day 58: Stock Goes Down

## The brief

A duka's app records orders, and the shopkeeper wants the stock count to stay right. On Day 51 the app's code was supposed to keep `orders_count` up to date, forgot once, and the numbers drifted. Today the **database** keeps the stock right, whoever writes the order: the app, a script, or someone typing SQL at midnight.

A **trigger** is SQL the database runs by itself when a row is inserted, updated or deleted.

## What you'll use

```sql
CREATE TRIGGER decrease_stock
AFTER INSERT ON orders              -- BEFORE or AFTER; INSERT, UPDATE or DELETE; which table
FOR EACH ROW                        -- once per row the statement touches
UPDATE items SET quantity = quantity - NEW.number WHERE name = NEW.item_name;
```

- **`NEW` and `OLD`** are the row as it will be and as it was. `INSERT` has only `NEW`, `DELETE` only `OLD`, and `UPDATE` both.
- **More than one statement** needs `BEGIN ... END`, and the `;` inside would end the `CREATE TRIGGER` too early in the `mysql` client. So change the client's delimiter for a moment:

  ```sql
  DELIMITER //
  CREATE TRIGGER log_stock_change AFTER UPDATE ON items FOR EACH ROW
  BEGIN
      IF NEW.quantity <> OLD.quantity THEN
          INSERT INTO stock_log (item_name, old_quantity, new_quantity) VALUES (NEW.name, OLD.quantity, NEW.quantity);
      END IF;
  END //
  DELIMITER ;
  ```

  `DELIMITER` is a command for the `mysql` client, not SQL. The server never sees it.
- **Refusing a change**: in a `BEFORE` trigger, `SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '...'` raises an error. The statement fails, and nothing it did is kept (InnoDB undoes the whole statement). `45000` means "an error the user defined".
- **Triggers chain**: inserting an order updates `items`, which fires `items`' update trigger. A trigger can't change the table that fired it, though (`ERROR 1442`).
- **Re-runnable**: `DROP TRIGGER IF EXISTS name;` first. MySQL has no `CREATE OR REPLACE TRIGGER`.
- `SHOW TRIGGERS;` lists them.
- **The other side**: triggers are invisible from the app's code. A newcomer runs an `UPDATE` and is surprised when three other tables change. Use them for rules that must *always* hold, and name them clearly.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS duka;"
tools/mysql.sh duka < phase-5-advanced-mysql/day-058-stock-goes-down/setup.sql
```

1. `starter/0-decrease_stock.sql`: orders take stock away.
2. `starter/1-log_stock_change.sql`: every real change of quantity is logged.
3. `starter/2-no_overselling.sql`: refuse orders bigger than the stock.
4. `starter/3-cancel_order.sql`: a deleted order puts its stock back.
5. `pytest phase-5-advanced-mysql/day-058-stock-goes-down`

Each file must be safe to run twice. Try them by hand: insert an order, then `SELECT * FROM items;` and `SELECT * FROM stock_log;`.

## The kata: Order Changed

In `starter/kata.sql`, write `adjust_stock`, which runs after an order is updated. The number might change (5 becomes 8: three more come off), the item might change (sugar back, rice off), or both. If only the number changes, make it one update, so the log gets one row and not two.

## When you're stuck

- **`ERROR 1064` near `END`, or the trigger stops halfway**: you need `DELIMITER //` before the `CREATE TRIGGER` with `BEGIN ... END`, and `DELIMITER ;` after.
- **`ERROR 1359: Trigger already exists`**: `DROP TRIGGER IF EXISTS` first.
- **`ERROR 1363: There is no OLD row in on INSERT trigger`**: inserts only have `NEW`.
- **The oversell check lets the order through**: it must be `BEFORE INSERT`. By the time an `AFTER` trigger runs, the stock has been taken already, by the other trigger.
- **The log has a row for Sugar 25 → 25**: wrap the insert in `IF NEW.quantity <> OLD.quantity`.
- **The kata takes the stock off twice when the item changes**: the old item gets `OLD.number` back, and the new item loses `NEW.number`.
