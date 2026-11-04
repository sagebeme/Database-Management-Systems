# Day 80: Postgres Superpowers

## The brief

The matatu app records a lot that doesn't fit neat columns. Each trip's record holds the driver, the seats, whether the matatu took M-Pesa at the door, every fare paid, sometimes the music. Each route is a list of stops. Passengers search the notices for "road closed". In MySQL you'd reach for extra tables, or JSON with awkward functions (Day 63). Postgres has three things built in that make this easy: **JSONB**, **arrays** and **full-text search**, and they can all be indexed.

## What you'll use

**JSONB** stores JSON parsed into a binary form, so it can be searched and indexed:

| | gives | example |
|---|---|---|
| `->` | JSON | `details -> 'fares'` is `[70, 70, 50]` |
| `->>` | text | `details ->> 'driver'` is `Otieno` |
| `@>` | contains | `details @> '{"cashless": true}'` |
| `?` | has the key | `details ? 'music'` |
| `jsonb_array_length(j)` | how many elements | |
| `jsonb_array_elements_text(j)` | one row per element, as text | `SELECT SUM(f::int) FROM jsonb_array_elements_text(...) AS f` |
| `jsonb_build_object('k', v, ...)`, `jsonb_agg(x ORDER BY ...)` | build JSON | |

Containment is exact about types: `{"cashless": "yes"}` doesn't contain `{"cashless": true}`.

A **GIN index** (`CREATE INDEX ... ON trips USING GIN (details)`) indexes every key and value inside the documents, so `@>` and `?` searches don't read every row.

**Arrays**: any type can be an array: `stops TEXT[]`. Write one as `'{Kencom,Westlands,"Kenyatta Avenue"}'` or `ARRAY['Kencom', 'Westlands']`.

- `'Westlands' = ANY (stops)`: is it in there?
- `cardinality(stops)`: how many (0 for an empty array; `array_length(stops, 1)` gives `NULL` instead).
- `unnest(stops)`: one row per element. `FROM routes, unnest(stops) AS stop` pairs every route with each of its stops.
- `stops[1]`: the first element. Arrays start at 1.

**Full-text search** understands language, not just characters:

```sql
SELECT to_tsvector('english', 'The Kencom stage is closing for a week');
-- 'close':4 'kencom':2 'stage':3 'week':7       words reduced to stems, little words dropped
SELECT to_tsquery('english', 'close & road');   -- & and, | or, ! not
```

`to_tsvector(...) @@ to_tsquery(...)` matches, so "closed", "closing" and "close" all match `close`. `ts_rank` scores matches, and a GIN index on `to_tsvector('english', body)` makes searching fast.

## Steps

```bash
tools/psql.sh matatu -f phase-7-beyond-mysql/day-080-postgres-superpowers/setup.sql
```

Look at the data first: `SELECT details FROM trips;`, `SELECT * FROM routes;`. Then:

1. `starter/0-cashless_trips.sql`: trips recorded as cashless, with the driver's name.
2. `starter/1-takings.sql`: passengers and takings per trip, from the `fares` array.
3. `starter/2-details_index.sql`: a GIN index on `details`.
4. `starter/3-via_westlands.sql`: routes through Westlands, with their number of stops.
5. `starter/4-busiest_stops.sql`: how many routes stop at each stop.
6. `starter/5-closures.sql`: notices about a road closed or closing.
7. `pytest phase-7-beyond-mysql/day-080-postgres-superpowers`

## The kata: Trips as JSON

In `starter/kata.sql`, return one row per route with its trips as a JSON array of `{"id", "driver"}` objects: the shape an API would send to the app. A route with no trips gets `[]`.

## When you're stuck

- **`operator does not exist: jsonb = boolean`**: compare with `@>` and a JSON document, or compare text: `details ->> 'cashless' = 'true'`.
- **Driver names come out with quotes, `"Otieno"`**: `->` returns JSON; `->>` returns text.
- **`function sum(jsonb) does not exist`**: turn each element into a number first: `jsonb_array_elements_text(...)`, then `::int`.
- **Trip 5 shows `NULL` takings**: the sum of no rows is `NULL`. `COALESCE(..., 0)`.
- **`ERROR: malformed array literal`**: arrays are written with braces, `'{a,b}'`, and elements with spaces need double quotes inside.
- **Notice 5 doesn't match**: search with `to_tsquery('english', ...)`, so "closing" is reduced to the same stem as "close". Plain `LIKE '%closed%'` misses it.
- **The kata gives `[null]` for an empty route**: a `LEFT JOIN` gives one row of `NULL`s. Use `FILTER (WHERE t.id IS NOT NULL)` on the aggregate and `COALESCE(..., '[]'::jsonb)`.
