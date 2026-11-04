# Day 57: Band Lifespans

## The brief

Dates are where simple-looking questions go wrong. "How old is she?" isn't `2026 - birth year` (has her birthday happened yet?). "When is it due?" crosses month ends. "How late is it?" depends on whether the book has come back. And someone born on 29 February needs an answer in 2027.

Two datasets today. Day 54's artists: how long has each Taarab act lasted? And a small library: due dates, late fines, members' ages, and (in the kata) everyone's next birthday.

**Everything is "as of 31 March 2026".** In real code you'd write `CURDATE()`, but then the right answer would change every day and the tests couldn't check it. Wherever a query says 2026-03-31, that's where `CURDATE()` would go.

## What you'll use

| You want | Write | Gives |
|---|---|---|
| a date plus or minus some time | `borrowed_on + INTERVAL 14 DAY` (or `DATE_ADD(borrowed_on, INTERVAL 14 DAY)`) | `2026-01-19` |
| days between two dates | `DATEDIFF(later, earlier)` | `25` (negative if the first is earlier) |
| whole years, months, ... between | `TIMESTAMPDIFF(YEAR, born_on, '2026-03-31')` | `41` (only *completed* years) |
| the weekday | `DAYNAME(d)` / `DAYOFWEEK(d)` | `Monday` / `2` (Sunday is 1) |
| part of a date | `YEAR(d)`, `MONTH(d)`, `DAY(d)` | |
| a date as text | `DATE_FORMAT(d, '%Y-%m')` | `2026-01` |
| the last day of its month | `LAST_DAY(d)` | `2026-02-28` |
| the smaller of two values | `LEAST(a, b)` (and `GREATEST`) | |

- **`YEAR` columns** (Day 54's `formed` and `split`) are just numbers of years, so `COALESCE(split, 2026) - formed` works.
- **Month and year arithmetic clamps.** `'2026-01-31' + INTERVAL 1 MONTH` is `2026-02-28`, and `'2004-02-29' + INTERVAL 23 YEAR` is `2027-02-28`. MySQL never invents a date that doesn't exist.
- **`TIMESTAMPDIFF(YEAR, ...)` is how to get an age.** `YEAR(today) - YEAR(born_on)` is a year too old for everyone whose birthday hasn't come yet this year.
- **Dates compare as dates**: `'2026-03-31'` in a comparison with a `DATE` column is read as a date.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS library;"
tools/mysql.sh library < phase-5-advanced-mysql/day-057-band-lifespans/setup.sql
```

1. `starter/0-lifespans.sql`: Taarab acts by how long they lasted.
2. `starter/1-due_dates.sql`: due date and weekday for every loan.
3. `starter/2-overdue.sql`: late loans, with days late and the fine (10 shillings a day, at most 500).
4. `starter/3-ages.sql`: ages on 31 March 2026.
5. `starter/4-loans_per_month.sql`: loans started per month.
6. `pytest phase-5-advanced-mysql/day-057-band-lifespans`

## The kata: Next Birthday

In `starter/kata.sql`, each member's next birthday on or after 31 March 2026 (a birthday today counts), and the days to go. Otieno's is today; Chebet was born on 29 February. Try "born_on plus their age in years": if that's already passed, add one more year.

## When you're stuck

- **A book returned on its due date shows up as late**: `DATEDIFF(returned, due)` is 0 then. Late means `> 0`.
- **The still-out loans are missing from the overdue list**: `returned_on` is `NULL`, and `DATEDIFF(NULL, ...)` is `NULL`. Use `COALESCE(returned_on, '2026-03-31')`.
- **Loans 9 and 10 show up as late**: they're still out, but not due until April. Their days late come out negative, so keep only rows `> 0`.
- **Everyone is a year older than the tests expect**: that's `YEAR() - YEAR()`. Use `TIMESTAMPDIFF`.
- **`DATEDIFF` gives negative numbers**: the later date goes first.
- **The kata gives Chebet `NULL` or 2027-03-01**: adding years to 29 February lands on 28 February in MySQL. Build the date with `+ INTERVAL n YEAR` rather than gluing text together with `CONCAT`.
