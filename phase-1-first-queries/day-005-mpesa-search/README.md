# Day 5: M-Pesa Search

## The brief

Faith wants to know where her money went in March. Her M-Pesa statement is a table with one row per transaction: a code, the kind (Sent, Received, Paybill, Till, Withdraw, Airtime), who it was with, the amount and the time. Her questions need more than one condition at once: "Sent *and* over 1,000", "Paybill *or* Till", "*not* airtime". Today you combine conditions.

`setup.sql` loads fourteen made-up transactions from late February to 1 April 2025.

## What you'll use

```sql
WHERE kind = 'Sent' AND amount > 1000            -- both must be true
WHERE kind = 'Paybill' OR kind = 'Till'          -- either is enough
WHERE kind IN ('Paybill', 'Till')                -- the same, shorter
WHERE NOT (kind = 'Airtime')                     -- the opposite
WHERE amount BETWEEN 500 AND 1000                -- 500 <= amount <= 1000, both ends included
WHERE counterparty LIKE 'KPLC%'                  -- starts with KPLC
WHERE counterparty LIKE '%Achieng'               -- ends with Achieng
WHERE code LIKE 'TC__AB%'                        -- _ is exactly one character
```

**`AND` binds tighter than `OR`**, the way `×` binds tighter than `+`. So

```sql
WHERE kind = 'Sent' OR kind = 'Received' AND amount > 2000
```

means `Sent OR (Received AND over 2000)`: it returns every send, however small. Put brackets around the `OR` when that's what you mean. When you mix `AND` and `OR`, always use brackets, even when they aren't needed, so the next person doesn't have to remember the rule.

**Date ranges: use `>=` the start and `<` the day after the end.**

```sql
WHERE happened_at BETWEEN '2025-03-01' AND '2025-03-31'      -- wrong for a DATETIME
```

`'2025-03-31'` means midnight at the *start* of 31 March, so this misses everything later that day. Write

```sql
WHERE happened_at >= '2025-03-01' AND happened_at < '2025-04-01'
```

which works for `DATE` and `DATETIME` alike, whatever the time of day.

**`NOT` with brackets**: "neither airtime nor under 50 bob" is `NOT (kind = 'Airtime' OR amount < 50)`, which is the same as `kind <> 'Airtime' AND amount >= 50`. Flipping a condition swaps `AND` and `OR` (De Morgan's laws).

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS mpesa;"
tools/mysql.sh mpesa < phase-1-first-queries/day-005-mpesa-search/setup.sql
```

1. `starter/0-big_sends.sql`: `code`, `counterparty`, `amount` of Sent transactions over 1,000.
2. `starter/1-bills_and_tills.sql`: `code`, `kind`, `counterparty` of Paybill or Till payments. Use `IN`.
3. `starter/2-march.sql`: `code` and `happened_at` of every transaction in March 2025.
4. `starter/3-kplc.sql`: `code`, `counterparty`, `amount` of payments to KPLC, prepaid or postpaid.
5. `starter/4-not_small_airtime.sql`: `code` and `kind` of transactions that are neither airtime nor under 50 bob.
6. `pytest phase-1-first-queries/day-005-mpesa-search`

## The kata: Brackets Matter

In `starter/kata.sql`, print `code` and `amount` of transactions that were Sent or Received, and over 2,000 bob.

## When you're stuck

- **Small sends show up in the kata**: brackets around the `OR`.
- **The March test misses TC31CX6ZA3**: that's 31 March at 18:20. Use `< '2025-04-01'` for the end.
- **The March test includes TD01QA2WS4**: that's 1 April at midnight. `<=` the 1st of April would include it; `<` doesn't.
- **`LIKE 'KPLC'` finds nothing**: without `%`, `LIKE` matches the whole value exactly.
- **The not-airtime test lets the 30-bob send through**: you wrote `kind <> 'Airtime' OR amount >= 50`. Flipping `OR` inside `NOT` gives `AND`.
