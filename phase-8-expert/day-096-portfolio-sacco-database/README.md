# Day 96: Portfolio: SACCO Database

## The brief

Umoja Boda SACCO has 400 riders and runs on a notebook and an Excel file that three treasurers edit. Last year two loans went out against the same guarantor's savings, and a member withdrew money that was holding up someone else's loan. They want a PostgreSQL database that makes those mistakes impossible, not just unlikely.

This is a portfolio day: no walkthrough. You get the client's rules and the interface their app will call. How you build it is yours. The tests are their acceptance checks. When it passes, put it on GitHub with a README of your own: it's the strongest thing in your portfolio so far.

**The rules**

1. A member has a name and a phone number like `2547XXXXXXXX` or `2541XXXXXXXX`, unique. They join today unless told otherwise.
2. Money moves only by deposit and withdrawal, recorded in a ledger that is never edited. Amounts are whole shillings, always positive.
3. A member can withdraw only their **free savings**: savings minus whatever they've guaranteed on loans that are still active.
4. A member may borrow up to **three times their savings**, and may have only one active loan at a time.
5. Their own savings cover part of the loan; **guarantors** pledge the rest. Each guarantor must have that much free savings. Nobody guarantees their own loan, and nobody is listed twice.
6. Interest is 10% flat, added when the loan is issued (whole shillings, rounded down): borrow 25,000, owe 27,500.
7. Repayments reduce the balance; nobody pays more than they owe. At zero the loan is **cleared** and the guarantors' savings are free again.
8. Two tellers working at the same moment must never break rules 3 to 5.

## What you'll use

The app calls exactly these, so the names matter:

| File | Must create |
|---|---|
| `schema.sql` | tables `members (id, name, phone, joined_on)`, `ledger (id, member_id, kind, amount, at)` with `kind` `'deposit'` or `'withdrawal'`, `loans (id, member_id, principal, balance, status, issued_at)` with `status` `'active'` or `'cleared'`, `guarantees (loan_id, member_id, amount)`, `repayments (id, loan_id, amount, at)`. Ids are generated. |
| `logic.sql` | functions `savings(member)`, `guaranteed(member)`, `free_savings(member)`, `deposit(member, amount)` and `withdraw(member, amount)` returning the new savings, `issue_loan(member, principal, guarantors integer[], amounts bigint[])` returning the loan id, `repay(loan, amount)` returning the balance left |
| `reports.sql` | views `member_summary (member_id, name, savings, loan_balance, guaranteed, free_savings)` and `monthly_flows (month 'YYYY-MM', deposits, withdrawals)` |

When a rule is broken, raise an error whose message contains these words, so the app can show it: `no such member`, `no such loan`, `insufficient` (savings), `active loan`, `limit`, `cover` (guarantees too small), `guarantor` (one can't afford it), `own` (guaranteeing yourself), `twice`, `length` (guarantor and amount arrays differ), `overpay`.

Everything from the course is fair game: `CHECK` constraints (Day 53), partial unique indexes, functions (Days 60 and 61, in PL/pgSQL now), `SELECT ... FOR UPDATE` (Day 71), lock ordering against deadlocks, views.

## Steps

1. Write the three files. Rebuild a scratch database and load them as you go:

   ```bash
   tools/psql.sh postgres -c "DROP DATABASE IF EXISTS umoja;" -c "CREATE DATABASE umoja;"
   for f in schema logic reports; do tools/psql.sh umoja -v ON_ERROR_STOP=1 -f phase-8-expert/day-096-portfolio-sacco-database/starter/$f.sql; done
   ```

2. `pytest phase-8-expert/day-096-portfolio-sacco-database`
3. Push it to your GitHub with a README: the rules, an ER diagram, and how you stopped the two-teller race.

## The kata: Dividends

At the AGM the SACCO pays a dividend on savings held at the end of the year. In `starter/kata.sql`, write `dividends(year integer, rate numeric)` returning `member_id`, `name`, `dividend`: savings at the end of that year times the rate (a percentage), rounded down to whole shillings, for members holding more than zero, in member order.

## When you're stuck

- **The two-teller test says the second withdrawal didn't wait**: two transactions each read the ledger, see enough money, and insert. Nothing conflicts, because inserts never block each other. Make every money-moving function lock the member's row first.
- **The tables accept a loan with a negative balance, or a cleared loan with money owed**: rules belong in `CHECK` constraints too (Day 53), not only in the functions. Someone will run an `UPDATE` by hand one day.
- **"Only one active loan" as a constraint**: a unique index with a `WHERE status = 'active'`.
- **Two loans sharing guarantors deadlock**: lock the members in id order.
- **A refused loan leaves guarantees behind**: check everything before inserting anything. (An error rolls back the whole statement anyway, but don't rely on the order you happened to write.)
- **`unnest` of two arrays**: `unnest(a, b) AS x (m, a)` pairs them up, in `FROM`.

## After it passes

Compare your design with the reference one, drawn as a diagram: [solution-schema.svg](solution-schema.svg). Look at what it chose to make a constraint (the composite key on `guarantees`, the partial unique index on `loans`) and what it left to the functions. Yours can differ and still be right; the tests are the judge.
