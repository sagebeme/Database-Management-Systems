# Day 65: Send Money

## The brief

Phase 6 is about what happens underneath: many people using the database at once, power cuts, and how the data actually sits on disk. It starts with the most important idea in databases: the **transaction**.

Sending money is two updates: take 2,000 from Wanjiku, give 2,000 to Chebet. If the server dies between them, 2,000 shillings have vanished. If a check fails after the first one, the same thing happens. Wallets, banks, SACCOs and M-Pesa all depend on one promise: **either all of it happens, or none of it does.**

## What you'll use

```sql
START TRANSACTION;
UPDATE accounts SET balance = balance - 2000 WHERE phone = '254711000001';
UPDATE accounts SET balance = balance + 2000 WHERE phone = '254733000003';
COMMIT;        -- make it permanent; ROLLBACK instead undoes everything since START TRANSACTION
```

**ACID**, the four promises a transaction makes:

| | Promise | Today |
|---|---|---|
| **A**tomicity | all or nothing | a failed step undoes the earlier ones |
| **C**onsistency | the rules (constraints) hold before and after | `CHECK (balance >= 0)` |
| **I**solation | transactions running at once don't see each other's half-done work | Days 66–72 |
| **D**urability | once committed, it survives a crash | Day 73 (the log) |

- **Autocommit**: by default every statement is its own transaction, committed straight away. `START TRANSACTION` turns that off until `COMMIT` or `ROLLBACK`.
- **Implicit commits**: `CREATE`, `ALTER`, `DROP` and `TRUNCATE` commit the open transaction first, and can't be rolled back. So does a second `START TRANSACTION`.
- **Savepoints** roll back part of a transaction: `SAVEPOINT p; ... ROLLBACK TO SAVEPOINT p;` undoes only what came after `p`.
- **In a procedure**, an error doesn't roll anything back by itself. Catch it, roll back, and pass it on:

  ```sql
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
      ROLLBACK;
      RESIGNAL;      -- the caller still gets the original error
  END;
  ```

- **`ROW_COUNT()`** is how many rows the last statement changed. `UPDATE ... SET balance = balance - 2000 WHERE phone = ? AND balance >= 2000` followed by "was `ROW_COUNT()` 0?" is the check *and* the change in one step. That matters on Day 66.
- **From Python** (the kata), PyMySQL is the same SQL: `conn.cursor().execute(...)` returns the number of rows changed, then `conn.commit()` or `conn.rollback()`.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS wallet;"
tools/mysql.sh wallet < phase-6-transactions-and-storage/day-065-send-money/setup.sql
```

1. `starter/0-send_money.sql`: `SendMoney`. The tests break the last step on purpose and check that nothing stayed changed.
2. `starter/1-reverse_transfer.sql`: `ReverseTransfer`.
3. `starter/answers.py`.
4. `pytest phase-6-transactions-and-storage/day-065-send-money`

Try a transaction by hand in two terminals: `START TRANSACTION;` and one `UPDATE` in the first, then `SELECT * FROM accounts;` in the second. The second can't see the change until the first commits.

## The kata: Pay Day

In `starter/pay_day.py`, write `pay_salaries(conn, payer, payments)`: pay everyone in **one** transaction, but skip any payment that can't be made (not enough left, or no such account) without losing the others. Use a savepoint before each payment. Watch the unknown phone: the payer has already been charged by the time you find out the receiver doesn't exist.

## When you're stuck

- **The atomicity test finds Mutua charged but Akinyi not paid**: your updates ran without a transaction, or the error skipped the `ROLLBACK`. Add the `EXIT HANDLER` with `ROLLBACK; RESIGNAL;`.
- **The error message is lost** (the caller sees success, or a different error): `RESIGNAL` passes the original on; a handler with only `ROLLBACK` swallows it.
- **`ERROR 3819: Check constraint 'accounts_chk_1' is violated`** instead of `Insufficient funds`: the `CHECK` caught it first, which is good, but the brief wants your message. Use `AND balance >= p_amount` and test `ROW_COUNT()`.
- **`ERROR 1305: SAVEPOINT payment does not exist`**: `ROLLBACK TO SAVEPOINT` must come after `SAVEPOINT`, inside the same transaction.
- **The kata's changes are gone after the test closes the connection**: you didn't `conn.commit()`. Closing an uncommitted connection rolls it back.
