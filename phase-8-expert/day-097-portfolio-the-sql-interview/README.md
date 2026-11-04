# Day 97: Portfolio: The SQL Interview

## The brief

You've made it to the technical round. The panel slides a laptop across: a PostgreSQL database from a boda and taxi app's first four months (riders, drivers, trips), and twenty questions. They're the questions data and backend interviews ask again and again, in one shape or another. Most can be done several ways; the panel cares that your answer is right on *any* data, not just the rows in front of you.

No walkthrough today. Each question names the pattern it's testing, so you know which part of the course to reread. Time yourself: in a real interview you'd have 60 to 90 minutes for about eight of these.

The tests run your answer on the data, then change the data (new riders and trips, a deleted range of ids, a banned rider, a new county, ties) and run it again. An answer that fits only today's rows fails the second run.

## What you'll use

```
riders  (id, name, phone, referred_by -> riders.id, banned)
drivers (id, name, county, vehicle 'boda' | 'tuktuk' | 'car')
trips   (id, rider_id, driver_id, requested_at timestamp, fare, status 'completed' | 'cancelled',
         payment 'mpesa' | 'cash', rating 1-5 or NULL)
```

Unless a question says otherwise, money and ratings count **completed trips only**. "Month" means a calendar month of `requested_at`, written `YYYY-MM`. Every answer has exactly the columns named, in that order.

| # | Question | Columns, order | Pattern |
|---|---|---|---|
| 1 | The second highest *distinct* fare. `NULL` if there's no second. | `second_highest` | `OFFSET`, or `max` below the `max` |
| 2 | Each driver's three highest-fare trips. A trip tied with the third is included. | `driver_id, trip_id, fare`; driver, fare highest first, trip | `rank()` |
| 3 | Phone numbers used by more than one rider. | `phone, riders`; phone | `GROUP BY ... HAVING` |
| 4 | Riders who have never completed a trip. | `id, name`; id | anti-join |
| 5 | Every streak of three or more consecutive days on which a driver completed at least one trip. | `driver_id, first_day, last_day, days`; driver, first day | gaps and islands |
| 6 | Revenue per month and its growth on the month before, as a percentage rounded to 1 place (`NULL` for the first month). | `month, revenue, growth`; month | `lag()` |
| 7 | Revenue per day (days with revenue only) and the running total. | `day, revenue, running_total`; day | `sum() OVER` |
| 8 | The median fare per vehicle type, rounded to 1 place. | `vehicle, median_fare`; vehicle | `percentile_cont` |
| 9 | Cohort retention: group riders by the month of their first completed trip (January to March). How many of each cohort completed a trip in the following month? Percentage to 1 place. | `cohort, riders, came_back, retention_percent`; cohort | cohorts |
| 10 | For each day from 1 to 7 January: the share of requests that were cancelled, ignoring requests by banned riders, to 2 places. Days with no requests don't appear. | `day, cancellation_rate`; day | conditional average |
| 11 | The top-earning driver in each county (all of them if tied). | `county, driver` (name), `earnings`; county, driver | rank per group |
| 12 | Every driver's completed trips split by payment, including drivers with none. | `driver_id, mpesa, cash, total`; driver | pivot with `FILTER` |
| 13 | For each driver with rated trips: how many rated trips scored below that driver's own average rating. | `driver_id, below_average`; driver | window average |
| 14 | The missing trip ids: each run of missing ids between 1 and the highest id. | `gap_start, gap_end`; gap start | `lead()` |
| 15 | Riders who completed trips in every type of vehicle the app has. | `rider_id`; rider | relational division |
| 16 | Completed trips on each day of January 2026 (0 on empty days) and the 7-day rolling average: that day and the six before it, counting only January days. To 2 places. | `day, trips, rolling_avg`; day | calendar plus `ROWS 6 PRECEDING` |
| 17 | For each month, the hour of the day (0 to 23) with the most requests of any status. On a tie, the earlier hour. | `month, hour, requests`; month | top 1 per group |
| 18 | Drivers in the top three earnings ranks, where equal earnings share a rank and the next rank follows on. | `rank, driver_id, earnings`; rank, driver | `dense_rank()` |
| 19 | The app double-submitted some requests: same rider, driver and `requested_at`. List the ids to delete, keeping the lowest id of each set. | `id`; id | `row_number()` |
| 20 | A rider's requests (any status) are one session while each comes within 30 minutes of the one before. For riders who ever made two requests in one session: their session and request counts. | `rider_id, sessions, requests`; rider | sessionisation |

## Steps

```bash
tools/psql.sh postgres -c "CREATE DATABASE boda;"
tools/psql.sh boda -f phase-8-expert/day-097-portfolio-the-sql-interview/setup.sql
tools/psql.sh boda -f phase-8-expert/day-097-portfolio-the-sql-interview/starter/q01.sql
```

1. Write each answer in `starter/q01.sql` to `starter/q20.sql`.
2. `pytest phase-8-expert/day-097-portfolio-the-sql-interview` (add `-k q05` for one question).

## The kata: Who Brought Whom

Riders join through referrals (`referred_by`). In `starter/kata.sql`, list every rider with the rider at the top of their referral chain (someone nobody referred) and how many steps up that is: `rider_id, root_id, depth`, by rider. A rider nobody referred is their own root, at depth 0.

## When you're stuck

- **1 returns 500 when two trips cost 500**: you want the second highest *distinct* fare. `DISTINCT`, or `max(fare) WHERE fare < (SELECT max(fare) ...)`.
- **2 shows only three rows for a driver with a tie**: `row_number()` breaks ties; `rank()` keeps them.
- **4 misses riders who only ever cancelled**: "never completed" isn't "never requested". Put the status in the subquery.
- **5, the trick**: number each driver's days 1, 2, 3 in date order. Within a run of consecutive days, the day minus its number stays the same. Group by that.
- **9 counts riders in the wrong cohort**: the cohort is the month of the *first* trip, so work that out per rider before anything else.
- **10's rates are all 0 or 1**: integer division. `avg(CASE ... THEN 1.0 ELSE 0 END)`.
- **12 misses a driver**: an inner join drops drivers with no trips. `LEFT JOIN`, with the status condition in `ON`, not `WHERE` (Day 20).
- **14 misses a gap at the start**: if id 1 is gone, nothing comes before it to have a `lead()`. Handle that case on its own.
- **15 is right until a new vehicle type appears**: compare with the number of types in `drivers`, not the number 3.
- **16's first days are wrong**: build the calendar with `generate_series`, `LEFT JOIN` the trips onto it, then the window.
- **17 returns two rows for a month**: `DISTINCT ON (month)` with `ORDER BY month, requests DESC, hour`.
- **20, the trick**: mark each request 1 if it starts a new session (no request before it, or more than 30 minutes since), else 0. A rider's sessions are the sum of the marks.
