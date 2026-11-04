# Day 11: Missing Phone Numbers

## The brief

Wekesa Hardware in Kitale sells cement and iron sheets on credit to builders it trusts. When the shop moved its customer book into a database, some details had never been collected: some customers have no phone on record, some no email, some no agreed credit limit yet. Those empty cells are **`NULL`**.

Mr Wekesa wants to call everyone, count what's missing, and work out the average credit limit. Every one of those questions goes subtly wrong if you treat `NULL` like a normal value. Today is about getting them right.

## What you'll use

**`NULL` means "unknown" or "not applicable".** It isn't `0`, it isn't `''`, and it isn't a value at all. So:

- **Any comparison with `NULL` is *unknown*, not true or false.** `NULL = NULL` is unknown. `referred_by <> 1` is unknown when `referred_by` is `NULL`. `WHERE` keeps only rows where the condition is *true*, so unknown rows quietly disappear. SQL has three truth values: true, false and unknown.

  | `a` | `b` | `a AND b` | `a OR b` |
  |---|---|---|---|
  | true | unknown | unknown | true |
  | false | unknown | false | unknown |
  | unknown | unknown | unknown | unknown |

  `NOT unknown` is still unknown.

- Test for it with `IS NULL` and `IS NOT NULL`.
- **Arithmetic with `NULL` gives `NULL`**: `credit_limit + 1000` is `NULL` when the limit is unknown.
- **Aggregates skip `NULL`s**: `COUNT(phone)` counts rows *with* a phone, while `COUNT(*)` counts all rows. `AVG(credit_limit)` averages only the known limits. Whether that's right depends on what `NULL` means: "not agreed yet" (skip it) or "no credit" (treat it as 0)?
- **`COALESCE(a, b, c)`** returns the first of its arguments that isn't `NULL`: `COALESCE(phone, email, 'no contact')`. MySQL also has `IFNULL(a, b)` for two arguments.
- **Sorting**: MySQL puts `NULL`s first in ascending order and last in descending order. To force them last whatever the direction, sort by `credit_limit IS NULL` first: it's `0` for known values and `1` for unknown ones.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS hardware;"
tools/mysql.sh hardware < phase-1-first-queries/day-011-missing-phone-numbers/setup.sql
```

1. `starter/0-no_phone.sql`: names of customers with no phone, alphabetical.
2. `starter/1-best_contact.sql`: every `name` and a `contact`: phone, else email, else `no contact`. Alphabetical.
3. `starter/2-what_we_know.sql`: one row with `customers`, `with_phone` and `with_email`.
4. `starter/3-average_credit.sql`: `avg_known` (unknown limits left out) and `avg_unknown_as_zero`, both rounded to 2 places.
5. `starter/4-not_referred_by_wanjiku.sql`: names of everyone *not* referred by Wanjiku (id 1), including people nobody referred. Alphabetical.
6. `pytest phase-1-first-queries/day-011-missing-phone-numbers`

## The kata: Unknowns Last

In `starter/kata.sql`, list `name` and `credit_limit`, biggest limit first, with unknown limits at the end, alphabetical among themselves. Note that Achola's limit is `0.00`, which is known: she has no credit, which isn't the same as "not decided".

## When you're stuck

- **`WHERE phone = NULL` finds nothing**: it never will. `IS NULL`.
- **The not-referred list is missing Wanjiku, Chepchumba and Mutiso**: nobody referred them, so `referred_by <> 1` is unknown for them. Add `OR referred_by IS NULL`.
- **`with_phone` says 8**: `COUNT(*)` counts rows. `COUNT(phone)` counts phones.
- **The NULLs come first in the kata**: sort by `credit_limit IS NULL` before `credit_limit DESC`.
- **Achola ends up with the unknowns**: you used `COALESCE(credit_limit, 0)` to sort. `0` is a real limit; the unknowns go after it.
