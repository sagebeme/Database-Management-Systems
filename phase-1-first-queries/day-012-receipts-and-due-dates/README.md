# Day 12: Receipts and Due Dates

## The brief

Neno Printers on Moi Avenue, Mombasa, prints wedding cards, menus and banners, and sends an invoice for each job with so many days to pay. The owner, Bi Rukia, wants the invoice table to answer the questions she asks every Monday: print me the receipt lines, when is each one due, who paid late and by how much, and who hasn't paid at all.

The answers are in the data, but not in any one column. You'll build them with **functions**: for text, for numbers and for dates, plus **`CASE`**, SQL's if-then-else.

## What you'll use

**Text**

```sql
CONCAT('Habari ', name, '!')           -- glue text together
UPPER(name), LOWER(name)
CHAR_LENGTH(name)                      -- characters (LENGTH counts bytes, which differs for é or emoji)
LEFT(code, 3), SUBSTRING(code, 4, 2)   -- the first 3 characters; 2 characters from position 4
SUBSTRING_INDEX('Fatma Said', ' ', 1)  -- everything before the first space: 'Fatma'
TRIM('  Fatma  '), REPLACE(phone, '+', '')
```

**Numbers**

```sql
ROUND(12.345, 2)        -- 12.35
FORMAT(18500, 2)        -- '18,500.00': text with thousands commas, for display only
CEIL(4.1), FLOOR(4.9)   -- 5, 4
```

**Dates**

```sql
DATE_ADD('2025-01-06', INTERVAL 14 DAY)   -- 2025-01-20 (also MONTH, YEAR, HOUR ...)
DATEDIFF('2025-02-03', '2025-01-27')      -- 7: days from the second to the first
DATE_FORMAT('2025-03-17', '%Y-%m')        -- '2025-03'
YEAR(d), MONTH(d), DAYNAME(d)             -- 2025, 3, 'Monday'
```

`CURDATE()` and `NOW()` give today's date and time. Today's files avoid them, so the answers don't change from one day to the next.

**`CASE`** picks a value. The first `WHEN` that's true wins:

```sql
CASE
    WHEN amount >= 10000 THEN 'big'
    WHEN amount >= 5000 THEN 'medium'
    ELSE 'small'
END AS size
```

Order the `WHEN`s carefully: put the `NULL` check first, because comparisons with `NULL` are never true (Day 11).

**Repeating yourself**: the due date appears in three places in your queries today. On Day 56 you'll name a calculation once with a CTE. For now, repeat it.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS printers;"
tools/mysql.sh printers < phase-1-first-queries/day-012-receipts-and-due-dates/setup.sql
```

All lists are in id order unless they say otherwise.

1. `starter/0-receipt_lines.sql`: one column `line`, like `FATMA SAID: KES 18,500.00`.
2. `starter/1-first_names.sql`: `id` and the customer's `first_name` (the part before the first space).
3. `starter/2-due_dates.sql`: `id` and `due_on`, which is `issued_on` plus `days_to_pay` days.
4. `starter/3-days_late.sql`: for invoices paid *after* their due date, `id` and `days_late`, latest first.
5. `starter/4-status.sql`: `id` and `status`: `unpaid` (no `paid_on`), `late` (paid after the due date) or `on time`.
6. `pytest phase-1-first-queries/day-012-receipts-and-due-dates`

## The kata: Invoices per Month

In `starter/kata.sql`, list each `month` (written `2025-01`) and the number of `invoices` issued in it, in month order.

## When you're stuck

- **`18500.00` without the comma**: use `FORMAT(amount, 2)`, not `ROUND`.
- **The days-late numbers are negative**: `DATEDIFF(later, earlier)`. The later date goes first.
- **Invoice 4 comes out late**: it was paid on the due date. Late means `paid_on > due_on`.
- **Unpaid invoices say `on time`**: `paid_on > ...` is unknown when `paid_on` is `NULL`, so they fall through to `ELSE`. Put `WHEN paid_on IS NULL` first.
- **`Mwanaisha Binti` as a first name**: `SUBSTRING_INDEX(customer, ' ', 1)` takes the part before the *first* space.
