# Day 52: Capstone: The Agent's Ledger

## The brief

Three M-Pesa agents (Mama Lucy Agencies in Kawangware, Baraka Mobile Shop in Githurai 45, Kilimani Cyber) used to keep their ledgers in exercise books, like the shop on Day 29. Their aggregator had someone type three days of them into one spreadsheet, now loaded as `ledger_raw`. Every column is text, and it shows:

```
'TJHV3GOWID', '01/10/2026 11:48', '512340', 'Mama Lucy Agencies ', 'Kawangware', '254745000505', 'Akinyi Atieno  ', 'deposit', '7,500', '50'
'TJYR6THVU1', '01/10/2026 11:40', '600218', 'Kilimani Cyber', 'Kilimani', '0768 000 707', 'Njeri Wambui ', 'deposit', '12,000', '50'
```

- The agent's name and location are repeated on every row, and so is the customer's name.
- Phones come as `0768 000 707`, `+254722000202` and `254745000505`.
- Dates are day/month/year text, types are `deposit`, `DEPOSIT` or `Withdrawal `, and amounts have commas.

Your job is the whole of Phase 4 in one go: find the dependencies, prove the design, build it with every rule the business has, move the data in clean, and show that nothing was lost.

## What you'll use

- **Days 41–49**: FDs, closure and keys, normal forms, 3NF synthesis.
- **Day 31**: `CHECK`, `ENUM`, foreign keys. **Day 27**: cleaning text on the way in.
- **New today, `STR_TO_DATE(text, format)`**: it reads a date written any way, the opposite of `DATE_FORMAT`. `STR_TO_DATE('01/10/2026 11:48', '%d/%m/%Y %H:%i')` gives `2026-10-01 11:48:00`. `%d` is the day, `%m` the month, `%Y` a 4-digit year, `%H` the hour (00–23) and `%i` the minutes.
- **Cleaning in a derived table** (Day 18) saves writing the same expression twice:

  ```sql
  SELECT ... FROM (SELECT ledger_raw.*, REPLACE(TRIM(phone), ' ', '') AS p FROM ledger_raw) AS r;
  ```

- **Phones**: once the spaces are gone, `+254…` loses its `+`, `0…` becomes `254…`, and `254…` stays as it is. (Daraja and the SMS gateways want `2547XXXXXXXX`, 12 digits, no `+`.)
- **Is commission derived?** It looks like it's worked out from the type and amount, but rates change. The commission on a transaction is what was *paid that day*, a fact of the transaction. So store it; don't recompute it. The same goes for prices on an order line.

**Table contract** (the tests check these names):

| Table | Columns | Rules |
|---|---|---|
| `agents` | `till`, `name`, `location` | one row per till; name and location required |
| `customers` | `phone`, `name` | one row per phone; phone matches `^254[17][0-9]{8}$`; name required |
| `transactions` | `code`, `done_at`, `till`, `phone`, `type`, `amount`, `commission` | code unique; `done_at` a required `DATETIME`; real agent and customer; type `Deposit` or `Withdrawal`; amount above 0; commission 0 or more; an agent with transactions can't be deleted |

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS ledger;"
tools/mysql.sh ledger < phase-4-normalisation/day-052-capstone-the-agents-ledger/setup.sql
```

1. **On paper first**, then `starter/answers.py`: the FDs, the key, the highest normal form, and the 3NF parts.
2. `starter/0-schema.sql`: the three tables, per the contract.
3. `starter/1-migrate.sql`: fill them from `ledger_raw`, cleaned. Agents first, then customers, then transactions (the foreign keys decide the order).
4. `starter/2-float.sql`: each agent's deposits, withdrawals and commission, zeros included.
5. `starter/3-rebuild.sql`: join it all back into the flat ledger, clean, oldest first, ties by code.
6. `pytest phase-4-normalisation/day-052-capstone-the-agents-ledger`

## The kata: Regulars

In `starter/kata.sql`, customers who used two or more different agents: `phone`, `name`, `agents`. Most agents first, ties by phone. With one table that would have been a puzzle; now it's a `GROUP BY`.

## When you're stuck

- **`ERROR 1062: Duplicate entry '254722000202' for key 'customers.PRIMARY'`**: the same customer came out twice, once as `Otieno Ouma` and once as `Otieno Ouma  `. `TRIM` the name before `DISTINCT`. The same goes for agents.
- **`ERROR 3819: Check constraint ... is violated`** on customers: a phone still has a space or a `+` in it. `REPLACE(TRIM(phone), ' ', '')` first, then fix the prefix.
- **`ERROR 1265: Data truncated for column 'type'`**: `'deposit'` and `'Withdrawal '` aren't in the `ENUM`. Compare `LOWER(TRIM(txn_type))` and write the proper spelling yourself.
- **`ERROR 1292: Truncated incorrect INTEGER value: '7,500'`**: `CAST` stops at the comma (in a plain `SELECT` it quietly gives 7). Remove the commas first.
- **`ERROR 1411: Incorrect datetime value ... for function str_to_date`**: the format doesn't fit the text. `%m` is the month number, `%i` is minutes (`%M` is the month's *name*), and the slashes and space must match too.
- **`ERROR 1452: Cannot add or update a child row`**: transactions went in before their agent or customer.
- **The answers test says a dependency doesn't hold**: `txn_type`, `amount` and `commission` hang off `code`, not off the phone or till. The same customer does many transactions.
