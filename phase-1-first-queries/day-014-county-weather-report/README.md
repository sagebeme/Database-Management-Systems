# Day 14: Capstone: County Weather Report

## The brief

You've been hired for a week by a farmers' cooperative that advises members across Kenya on what to plant and when. They have a year of weekly readings from one weather station in each of eight counties, from hot, dry Turkana to the cool highlands of Nyandarua, and they want a report: where's hottest, which months bring the rain, where readings are missing, how much the temperature swings.

There's no walkthrough today. Everything you need is from Days 1 to 13.

`setup.sql` loads 416 readings: every Wednesday of 2024, for eight stations. **The data is simulated**: the places are real and the numbers follow each place's climate, but they were generated, not measured. A few rainfall readings are missing (`NULL`).

```
+---------+------------------+-------------+-------+-------+---------+
| county  | station          | recorded_on | max_c | min_c | rain_mm |
+---------+------------------+-------------+-------+-------+---------+
| Mombasa | Moi Airport      | 2024-01-03  |  30.9 |  25.2 |     2.0 |
| Nairobi | Dagoretti Corner | 2024-01-03  |  25.4 |  14.2 |     0.2 |
...
```

## What you'll use

Everything from Phase 1: `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`, aggregates, `GROUP BY`, `HAVING`, `NULL` handling, date and text functions, and `CASE`. No new syntax.

Check your answers against your own common sense as you go: Turkana should be hotter than Nyandarua, and the long rains (March to May) should be wet.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS weather;"
tools/mysql.sh weather < phase-1-first-queries/day-014-county-weather-report/setup.sql
```

Each file is one query. Column names and orders are part of the answer.

| File | The question | Columns |
|---|---|---|
| `0-average_highs.sql` | Each county's average daily high, hottest first | `county`, `avg_max` (1 decimal place) |
| `1-cool_season_top3.sql` | The three counties with the highest average high in July and August, hottest first | `county`, `avg_max` (1 place) |
| `2-record_highs.sql` | Each county's hottest reading, alphabetical by county | `county`, `hottest` |
| `3-wettest_months.sql` | The three wettest months across all counties, wettest first | `month` (like `2024-05`), `rain` (total mm) |
| `4-gaps.sql` | Counties with missing rainfall readings, most first, ties alphabetical | `county`, `missing` |
| `5-swing.sql` | Each county's hottest high minus its coldest low, biggest first, ties alphabetical | `county`, `swing` |
| `6-climate_labels.sql` | Each county with a label: `hot` (average high 30 or more), `warm` (24 or more), else `cool`. Alphabetical | `county`, `avg_max` (1 place), `label` |
| `7-report_lines.sql` | One line per county, alphabetical, like `Kakamega: 2,102.6 mm of rain in 2024` | `line` |

Sort and filter on exact values; round only what you display.

```bash
pytest phase-1-first-queries/day-014-county-weather-report
```

The tests check each answer twice: once on the data as given, and once after changing it (a July heatwave in Nyandarua, a flood week in Garissa, lost readings in Mombasa, a frost in Ol Kalou). A query that's right for the right reasons passes both.

## The kata: Coldest Night

In `starter/kata.sql`, print the single coldest reading of the year: `county`, `recorded_on` and `min_c`.

## When you're stuck

- **The July–August test fails only after the data changes**: you're probably filtering with the right months but sorting by the rounded value, or your date range misses the 31st of August. Use `>= '2024-07-01'` and `< '2024-09-01'`.
- **`missing` is always 0**: `COUNT(rain_mm)` skips `NULL`s, so `COUNT(*) - COUNT(rain_mm)` counts them.
- **A county with no gaps shows `0`**: keep only groups with gaps, using `HAVING`.
- **The labels are off by one county**: compare the *unrounded* average with 30 and 24.
- **`FORMAT` gives `2102.6` with no comma**: check you wrote `FORMAT(SUM(rain_mm), 1)`. `ROUND` doesn't add commas.
- **Done?** Go back to Day 1 and skim each README. You know all of it now.
