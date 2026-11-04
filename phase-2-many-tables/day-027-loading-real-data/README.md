# Day 27: Loading Real Data

## The brief

Real data rarely arrives as `INSERT` statements. It comes as a spreadsheet export: a CSV file with a header row, quotes around some fields, thousands separators in the numbers, and names with apostrophes and dashes. A county planning team wants Kenya's 2019 census figures in MySQL so they can query them, and the file is `counties.csv`, in this folder.

**This is real data**: the population, total area and land area of all 47 counties from the 2019 Kenya Population and Housing Census (KNBS, Volume I), as tabulated on Wikipedia's *List of counties of Kenya by area* (fetched 4 November 2026). The codes, former provinces and capitals come from Wikipedia's *Counties of Kenya*.

One more real-world lesson came for free. That second page lists Turkana's 2019 population as 1,504,976, but KNBS published **926,976** (Turkana's leaders disputed the count as too low, but that is the official figure). The page's 47 rows add up to 48,142,296, not the published 47,564,296. That's how the mistake showed up. `counties.csv` uses the KNBS figure. **Always check an import against a total someone published.**

```
code,county,former_province,capital,total_area_km2,land_area_km2,population_2019
001,Mombasa,Coast,Mombasa,216,151,"1,208,333"
006,Taita–Taveta,Coast,Mwatate,"17,120","17,084","340,671"
```

## What you'll use

```sql
LOAD DATA LOCAL INFILE 'path/to/file.csv'
INTO TABLE t
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES                                    -- skip the header
(code, name, @raw_population)                     -- file columns, in order
SET population = REPLACE(@raw_population, ',', '');
```

- **`LOCAL`** means the file is on *your* machine, and the `mysql` client sends it. A relative path is relative to the folder you ran the client from (the course folder, for us). Without `LOCAL`, the *server* reads the file from its own disk, which is usually locked down (`secure_file_priv`).
- **`OPTIONALLY ENCLOSED BY '"'`** handles fields wrapped in quotes, so the comma inside `"1,208,333"` isn't taken as a separator.
- **The column list maps file columns to table columns.** A `@name` reads a column into a variable instead, so `SET` can clean it before it lands. `REPLACE(@x, ',', '')` strips the thousands commas.
- **`CHARACTER SET utf8mb4`** reads the file as UTF-8, so the en dash in *Taita–Taveta* arrives intact (Day 13).
- **Windows files** end lines with `\r\n`. If the last column of every row looks odd, use `LINES TERMINATED BY '\r\n'`.
- **`LOCAL` loads don't stop on bad values.** MySQL turns each one into a *warning*, bends the value to fit and carries on: `"1,208,333"` loaded into an `INT` column becomes `1`, with no error. Run `SHOW WARNINGS;` right after a load. A clean load has none.
- **Density depends on the denominator.** Mombasa is 30% water, so it's the most crowded county per km² of *land* but second to Nairobi per km² of *total* area. Say which you mean.

## Steps

Run everything from the course folder, so the path in `LOAD DATA` works:

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS census;"
```

1. `starter/0-counties_table.sql`: create `counties`: `code` (`CHAR(3)`, primary key), `name` (`VARCHAR(40)`, required, unique), `former_province` (`VARCHAR(20)`), `capital` (`VARCHAR(40)`), `total_area_km2`, `land_area_km2` and `population` (`INT`). All required.
2. `starter/1-load_counties.sql`: load `phase-2-many-tables/day-027-loading-real-data/counties.csv`, stripping the thousands commas. Run it with `tools/mysql.sh census < phase-2-many-tables/day-027-loading-real-data/starter/1-load_counties.sql`.
3. `starter/2-check_the_load.sql`: `counties` (how many) and `population` (the total). Compare with 47 and 47,564,296.
4. `starter/3-most_crowded.sql`: the 5 most crowded counties, by people per km² of **land**: `county`, `density` (a whole number). Most crowded first.
5. `starter/4-province_totals.sql`: for each former province: `former_province`, `counties`, `population`. Most people first.
6. `pytest phase-2-many-tables/day-027-loading-real-data`

## The kata: Counties on the Water

In `starter/kata.sql`, list the counties where water is at least 10% of the total area: `county`, `water_percent` (1 decimal place). Most water first.

## When you're stuck

- **`ERROR 3948: Loading local data is disabled`**: the server needs `local_infile=ON`. The course server has it; `tools/mysql.sh` turns it on for the client.
- **`File 'counties.csv' not found`**: the path is relative to where you ran the client. Run from the course folder.
- **`ERROR 2068: LOAD DATA LOCAL INFILE file request rejected`**: your client has local files turned off. Use `tools/mysql.sh`, which passes `--local-infile=1`.
- **The load works but the numbers are tiny (Mombasa has 1 person)**: MySQL read `"1,208,333"` up to the first comma and only warned you. Load into a `@variable` and `REPLACE` the commas.
- **The first row is `code, county, ...`**: add `IGNORE 1 LINES`.
- **Taita–Taveta arrives as `Taitaâ€“Taveta`**: add `CHARACTER SET utf8mb4`.
