# Day 28: Capstone: The Riverwood Report

## The brief

Riverwood Plus has its first board meeting next week, and Brenda wants a report: what the catalogue looks like, what viewers rate, what they save, and which titles they're asking for that the app doesn't carry yet. You're the one writing the queries.

There's no walkthrough today. Everything you need is from Days 15 to 27: keys, joins (inner and outer), subqueries, many-to-many through a junction table, anti-joins, and `GROUP_CONCAT`.

`setup.sql` loads the whole Riverwood database:

| Table | Holds |
|---|---|
| `tv_shows` | 13 invented shows: `id`, `title`, `first_aired`, `channel` |
| `tv_genres` | 11 genres: `id`, `name` |
| `tv_show_genres` | which show has which genres: `show_id`, `genre_id` |
| `tv_show_ratings` | one row per vote out of 10: `show_id`, `rate` |
| `watchlist` | viewers' saved shows: `viewer`, `show_id` (`NULL` when Riverwood doesn't have it), `requested_title` |

## What you'll use

Everything from Phase 2, and no new syntax. Before each query, say out loud which tables the answer lives in and which rows might have no match. Most mistakes today are a missing `LEFT JOIN` or a join that multiplies rows.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS riverwood;"
tools/mysql.sh riverwood < phase-2-many-tables/day-028-capstone-the-riverwood-report/setup.sql
```

Each file is one query. Column names and orders are part of the answer.

| File | The question | Columns |
|---|---|---|
| `0-show_list.sql` | Every show with its genres (alphabetical, joined by ', '; NULL if none). Alphabetical by title. | `title`, `genres` |
| `1-channel_lineup.sql` | Each channel and how many shows it has. Alphabetical. | `channel`, `shows` |
| `2-genre_counts.sql` | Every genre and how many shows it has, zero included. Most first, ties alphabetical. | `genre`, `shows` |
| `3-comedies_by_rating.sql` | Rated comedies and their rating sums. Highest first, ties alphabetical. | `title`, `rating` |
| `4-unrated.sql` | Shows nobody has rated yet. Alphabetical. | `title` |
| `5-not_drama.sql` | Shows that are not dramas, shows with no genre included. Alphabetical. | `title` |
| `6-watchlist_counts.sql` | Every show and how many times it has been saved to a watchlist, zero included. Most first, ties alphabetical. | `title`, `saves` |
| `7-wanted_titles.sql` | Titles viewers saved that Riverwood doesn't carry, with how many times each was asked for. Most first, ties alphabetical. | `requested_title`, `requests` |
| `8-akinyi_genres.sql` | The genres of the shows on akinyi's watchlist, each once. Alphabetical. | `genre` |
| `9-channel_scores.sql` | Each channel's average vote across all its shows' ratings (2 places). Channels with no votes are left out. Best first, ties alphabetical. | `channel`, `average` |
| `10-best_in_genre.sql` | For each genre with rated shows, the show with the highest rating sum (all of them on a tie). Ordered by genre, then title. | `genre`, `title`, `rating` |
| `11-watchlist_lines.sql` | One line per viewer, alphabetical, listing what they saved (the show title, or the requested title when Riverwood lacks it), alphabetical: like 'akinyi: Nairobi Nights, Siri za Lamu'. | `line` |

```bash
pytest phase-2-many-tables/day-028-capstone-the-riverwood-report
```

The tests check every answer twice: on the data as given, and after a shake-up (a new comedy, Mwisho wa Reli finding its genres and first votes, Jiko Wars losing its votes, a tie for best Crime show, and new watchlist requests). A query that's right for the right reasons passes both.

## The kata: Twins

In `starter/kata.sql`, find pairs of different shows with exactly the same set of genres (at least one genre each): `show_a`, `show_b`, with `show_a` alphabetically before `show_b`. Ordered by `show_a`, then `show_b`.

## When you're stuck

- **A show or genre with no match is missing**: every join after the first `LEFT JOIN` on that path must be a `LEFT JOIN` too.
- **Counts are too big**: a join to ratings or the watchlist makes one row per vote or save. Count the column you mean (`COUNT(w.id)`), or `DISTINCT`.
- **`5-not_drama` includes Nairobi Nights**: it has a Crime row that isn't Drama. Ask "is there a Drama row for this show?" with `NOT EXISTS`.
- **`10-best_in_genre` drops a show only after the shake-up**: on a tie you must keep both. Compare each show's sum with the genre's `MAX` instead of using `LIMIT 1`.
- **`11-watchlist_lines` has a blank for chebet's third save**: the title comes from `tv_shows` *or* `requested_title`. `COALESCE(a, b)` picks the first that isn't `NULL`.
- **The kata pairs a show with itself, or lists each pair twice**: join on `a.title < b.title`. To compare genre sets, turn each show's genre ids into one string with `GROUP_CONCAT(... ORDER BY ...)` in a derived table.
- **Done?** That's Phase 2. Phase 3 steps back from SQL to design: how to decide what the tables should be before you write any.
