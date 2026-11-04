# Day 23: Ratings

## The brief

Riverwood Plus lets viewers rate a show out of 10, and Brenda wants a leaderboard for the home page: which shows and genres viewers like most. The trouble with leaderboards is fairness. A show with seven votes beats one with four on a plain total, a show with one perfect 10 tops a list sorted by average, and a show with no votes yet still deserves a row saying so.

Today puts joins and `GROUP BY` together across three and four tables.

`setup.sql` adds `tv_show_ratings`, with one row per vote (`show_id`, `rate`). *Mwisho wa Reli* is too new to have any.

## What you'll use

Join down to the rows you want to count, then group by the thing you're ranking:

```sql
SELECT g.name, COUNT(*) AS votes
FROM tv_genres AS g
JOIN tv_show_genres AS sg ON sg.genre_id = g.id   -- genre -> its shows
JOIN tv_show_ratings AS r ON r.show_id = sg.show_id  -- show -> its votes
GROUP BY g.id, g.name;
```

- **Every join multiplies rows.** A show with 3 genres and 6 votes becomes 18 rows when you join both. That's right when you rank genres: each genre gets that show's 6 votes. But a "per show" total taken from that join counts every vote three times. Join only the tables your question needs.
- **Group by the id, not just the name.** Two shows could share a title one day; `GROUP BY s.id, s.title` keeps them apart.
- **`HAVING` filters groups**: `HAVING COUNT(*) >= 5` drops shows with too few votes to judge. It can compare with a subquery too: `HAVING AVG(rate) > (SELECT AVG(rate) FROM tv_show_ratings)`.
- **Sort by the exact value, display the rounded one.** `ORDER BY AVG(r.rate) DESC` sorts 8.71 above 8.709; sorting by the rounded column can tie them.
- **Counting zero** needs a `LEFT JOIN` and `COUNT(r.show_id)` (Day 20). `COUNT(*)` would give the unrated show a 1.
- **An average of totals** needs the totals first, in a derived table (Day 18).

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS riverwood;"
tools/mysql.sh riverwood < phase-2-many-tables/day-023-ratings/setup.sql
```

The tests add new votes and check your answers again.

1. `starter/0-rating_shows.sql`: `title`, `rating` (the sum of its votes) for every rated show. Highest first, ties alphabetical.
2. `starter/1-rating_genres.sql`: `name`, `rating` (the sum of the votes for its shows) for every rated genre. Highest first, ties alphabetical.
3. `starter/2-fair_averages.sql`: for shows with at least 5 votes: `title`, `average` (rounded to 2 places), `votes`. Best average first, ties alphabetical.
4. `starter/3-votes_per_show.sql`: every show with its number of `votes`, zero included: `title`, `votes`. Most first, ties alphabetical.
5. `starter/4-above_average_genres.sql`: genres whose votes average more than the average of all votes: `genre`, `average` (2 places). Best first, ties alphabetical.
6. `pytest phase-2-many-tables/day-023-ratings`

## The kata: Above the Average Show

In `starter/kata.sql`, list the shows whose rating sum beats the average of all rated shows' sums: `title`, `rating`. Highest first, ties alphabetical.

## When you're stuck

- **Your per-show totals are two or three times too big**: you joined the genres too. Step 1 needs only shows and ratings.
- **Mwisho wa Reli shows 1 vote**: count `r.show_id`, not `*`.
- **`ERROR 1111: Invalid use of group function`**: aggregate conditions go in `HAVING`, not `WHERE`.
- **Two shows swap places only after the new votes**: you sorted by the rounded `average`. Sort by `AVG(r.rate)` itself.
- **The kata includes almost every show**: you compared with the average *vote* (about 7), not the average *total* (about 42).
