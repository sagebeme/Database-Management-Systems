# Day 61: Average Scores

## The brief

The coding school from Day 60 shows each student's average on their dashboard, stored in `users.average_score`. Today you write the jobs that keep it right:

- A plain average for one student.
- A **weighted** average: the Normalisation project counts three times as much as SQL basics, so a 70 there hurts more.
- The same for *everyone* at once, which brings up a question every database person meets: loop over the rows one by one, or say it in one statement?

Along the way you'll write **functions** (procedures that return a value you can use inside a query), starting with a safe division.

## What you'll use

**A function** returns one value, and you use it like a built-in:

```sql
DELIMITER //
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT
DETERMINISTIC
BEGIN
    IF b = 0 THEN
        RETURN 0;
    END IF;
    RETURN a / b;
END //
DELIMITER ;

SELECT SafeDiv(score, 0) FROM corrections;
```

- **`DETERMINISTIC`** promises that the same inputs always give the same result. With binary logging on, MySQL refuses functions that don't declare what they do (`ERROR 1418`), unless the server sets `log_bin_trust_function_creators`, as the course's does. Declare it anyway, honestly: `DETERMINISTIC`, `NO SQL`, `READS SQL DATA`.
- **Procedure or function?** A function returns a value and can go inside a `SELECT`. A procedure is `CALL`ed, can change tables freely, and can return rows. In MySQL a function can't return a result set.

**A weighted average** is `SUM(score * weight) / SUM(weight)`. Wanjiku: (80×1 + 96×2 + 70×3) / (1 + 2 + 3) = 80.33.

**A cursor** walks a query's rows one at a time inside a procedure:

```sql
DECLARE done BOOLEAN DEFAULT FALSE;
DECLARE next_id INT;
DECLARE everyone CURSOR FOR SELECT id FROM users;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;   -- when FETCH runs out of rows

OPEN everyone;
read_loop: LOOP
    FETCH everyone INTO next_id;
    IF done THEN LEAVE read_loop; END IF;
    CALL ComputeAverageWeightedScoreForUser(next_id);
END LOOP;
CLOSE everyone;
```

The `DECLARE`s go in that order: variables, then cursors, then handlers.

**Row by row is slow by slow.** A cursor runs one `UPDATE` per user, which is fine for 4 users and painful for 4 million. SQL is built to work on whole sets at once. Most cursors can be replaced by one statement, and that's the kata. Keep cursors for jobs that really are one-at-a-time, like calling a procedure that has to run per row.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS school;"
tools/mysql.sh school < phase-5-advanced-mysql/day-061-average-scores/setup.sql
```

1. `starter/0-average_score.sql`: `ComputeAverageScoreForUser`.
2. `starter/1-safe_div.sql`: `SafeDiv`.
3. `starter/2-weighted_average.sql`: `ComputeAverageWeightedScoreForUser`.
4. `starter/3-all_users_cursor.sql`: `ComputeAverageWeightedScoreForUsers`, with a cursor.
5. `starter/4-grade.sql`: `Grade(score)`, a letter.
6. `pytest phase-5-advanced-mysql/day-061-average-scores`

## The kata: Same Answer, No Loop

In `starter/kata.sql`, write `ComputeAllInOneGo()`: every user's weighted average in **one `UPDATE`**, with no cursor, no loop and no `CALL`. Students with no corrections get 0. Hint: `UPDATE users AS u LEFT JOIN (a derived table of weighted averages) AS w ON ... SET ...`.

## When you're stuck

- **Mutua's average is `NULL`, or the update fails on him**: `AVG` of no rows is `NULL`, and `average_score` is `NOT NULL`. Use `COALESCE(..., 0)`.
- **`ERROR 1418: This function has none of DETERMINISTIC, NO SQL, or READS SQL DATA`**: add `DETERMINISTIC`.
- **`ERROR 1338: Cursor declaration after handler declaration`**: the order is variables, cursors, handlers.
- **The cursor loop never ends, or processes the last user twice**: check `done` straight after `FETCH`, before using the value.
- **`ERROR 1329: No data - zero rows fetched`**: the `CONTINUE HANDLER FOR NOT FOUND` is missing.
- **`Grade(79.99)` gives `'A'`**: the parameter is an `INT`, so 79.99 was rounded to 80 on the way in. Use `DECIMAL(5, 2)`.
- **The kata leaves Mutua's old average**: a plain `JOIN` skips users with no corrections. Use `LEFT JOIN` and `COALESCE`.
