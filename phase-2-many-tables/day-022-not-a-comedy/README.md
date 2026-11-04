# Day 22: Not a Comedy

## The brief

Brenda at Riverwood Plus is planning a "no laughing matter" week on the home page and needs the shows that are *not* comedies. Her team has three more questions of the same shape: which genres a show doesn't have yet, which shows and genres are unused, and which shows nobody has saved to their watchlist.

Each one asks for rows with **no match** somewhere else. That's an **anti-join**, and there are three ways to write one. One of them has a trap that hands you an empty result and no error.

`setup.sql` loads Riverwood with genres, ratings, and a new `watchlist` table. When a viewer saves a title Riverwood doesn't carry yet, `show_id` is `NULL` and `requested_title` holds what they typed.

## What you'll use

All three below find towns with no shops, in yesterday's terms:

```sql
-- 1. NOT IN a list
SELECT name FROM towns WHERE id NOT IN (SELECT town_id FROM shops);

-- 2. NOT EXISTS a matching row (correlated, Day 18)
SELECT name FROM towns AS t
WHERE NOT EXISTS (SELECT 1 FROM shops AS s WHERE s.town_id = t.id);

-- 3. LEFT JOIN, keep the unmatched (Day 20)
SELECT t.name FROM towns AS t
LEFT JOIN shops AS s ON s.town_id = t.id
WHERE s.id IS NULL;
```

`EXISTS` only cares whether the subquery returns a row, so `SELECT 1` is the usual thing to write inside it.

**The `NOT IN` trap.** `x NOT IN (1, 2, NULL)` means `x <> 1 AND x <> 2 AND x <> NULL`. The last part is *unknown* for every `x` (Day 11), so the whole thing is never true and the query returns **no rows at all**, with no error. If the subquery's column can hold `NULL`, use `NOT EXISTS`, or add `WHERE column IS NOT NULL` inside. `NOT EXISTS` doesn't have the problem: a `NULL` simply never matches.

**"Not a comedy" is not "a genre other than comedy."** *Matatu Kings* is Action **and** Comedy. `WHERE g.name <> 'Comedy'` keeps its Action row, so it slips into your list. Ask the question the other way round: find the comedies, then take every show *not in* that set.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS riverwood;"
tools/mysql.sh riverwood < phase-2-many-tables/day-022-not-a-comedy/setup.sql
```

Look things up by name. The tests change the data after the first check.

1. `starter/0-not_a_comedy.sql`: `title` of every show that isn't a comedy, including shows with no genre. Alphabetical.
2. `starter/1-not_my_genres.sql`: genres *Fundi Hacker* doesn't have: `name`, alphabetical.
3. `starter/2-shows_without_genres.sql`: `title` of shows with no genre, with a `LEFT JOIN`. Alphabetical.
4. `starter/3-unused_genres.sql`: `name` of genres no show has, with `NOT EXISTS`. Alphabetical.
5. `starter/4-nobody_saved.sql`: `title` of shows nobody has on their watchlist, alphabetical. Try `NOT IN` first and see what happens.
6. `pytest phase-2-many-tables/day-022-not-a-comedy`

## The kata: Channels Without Laughs

In `starter/kata.sql`, list the channels none of whose shows is a comedy: `channel`, alphabetical.

## When you're stuck

- **Matatu Kings is in your not-a-comedy list**: you kept its Action row. Exclude shows whose id is in the set of comedies.
- **Mwisho wa Reli is missing**: an inner join to the genres drops the show with no genre. Work from `tv_shows` alone and test membership.
- **Step 5 returns nothing**: that's the trap. `watchlist.show_id` holds a `NULL`. Use `NOT EXISTS`.
- **Every genre is listed in step 2**: the `NOT EXISTS` subquery needs both conditions: the genre matches the outer row (`sg.genre_id = g.id`) *and* the show is *Fundi Hacker*.
- **The kata lists Jamii TV**: you found channels that have *a* show which isn't a comedy. You want channels where *no* show is one.
