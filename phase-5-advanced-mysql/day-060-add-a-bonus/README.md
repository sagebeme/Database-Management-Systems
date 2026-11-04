# Day 60: Add a Bonus

## The brief

A coding school stores marks in three tables: `users`, `projects` and `corrections` (one score per user per project). Mentors keep asking for the same jobs:

- "Give Mutua 77 on the new Indexes project." That project doesn't exist yet, so someone has to create it first, then look up its id, then insert the score. Three steps, done by hand, wrong one time in ten.
- "How many corrections does Wanjiku have?"
- "Rename *Joins* to *Joins and subqueries*." But not if the new name is taken.

A **stored procedure** is a named program kept *in* the database: the steps are written once, and everyone runs them with `CALL AddBonus(4, 'Indexes', 77);`.

## What you'll use

```sql
DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER //
CREATE PROCEDURE AddBonus(IN p_user_id INT, IN p_project_name VARCHAR(60), IN p_score INT)
BEGIN
    INSERT INTO projects (name)
    SELECT p_project_name FROM DUAL
    WHERE NOT EXISTS (SELECT 1 FROM projects WHERE name = p_project_name);

    INSERT INTO corrections (user_id, project_id, score)
    SELECT p_user_id, id, p_score FROM projects WHERE name = p_project_name;
END //
DELIMITER ;

CALL AddBonus(4, 'Indexes', 77);
```

- **Parameters**: `IN` (the default) passes a value in. `OUT` hands one back in a session variable: `CALL CountCorrections(1, @n); SELECT @n;`. `INOUT` does both.
- **Name parameters so they can't be confused with columns.** Inside `WHERE name = name`, both are the parameter, so it's always true. Prefix them (`p_project_name`) or pick different words.
- **Local variables**: `DECLARE project INT DEFAULT NULL;` goes at the very top of `BEGIN`. Fill one with `SELECT id INTO project FROM ...`. If the `SELECT` finds no rows, the variable keeps its old value (and you get a "no data" warning).
- **Control flow**: `IF ... THEN ... ELSEIF ... ELSE ... END IF;`, and `SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '...'` (Day 58) to refuse.
- **A procedure can return rows**: a plain `SELECT` inside it is sent to whoever called it. `LIMIT how_many` can use a parameter here.
- `SHOW PROCEDURE STATUS WHERE Db = DATABASE();` lists them, and `SHOW CREATE PROCEDURE AddBonus;` shows one.
- **Procedures or app code?** Procedures keep a multi-step change in one place, next to the data, and save round trips. But they're harder to test, version and debug than app code, and they tie you to one database. Many teams use them sparingly, for jobs like today's.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS school;"
tools/mysql.sh school < phase-5-advanced-mysql/day-060-add-a-bonus/setup.sql
```

1. `starter/0-add_bonus.sql`: `AddBonus`, creating the project if needed.
2. `starter/1-count_corrections.sql`: `CountCorrections`, with an `OUT` parameter.
3. `starter/2-top_scorers.sql`: `TopScorers`, which returns rows.
4. `starter/3-rename_project.sql`: `RenameProject`, refusing bad renames.
5. `pytest phase-5-advanced-mysql/day-060-add-a-bonus`

## The kata: Curve the Marks

In `starter/kata.sql`, write `CurveProject(project_name, target)`. If the project's average is below the target, add the difference (rounded to the nearest point) to every score on it, but never past 100. If it's already at or above the target, leave it. Joins averages 76.33; curving it to 90 adds 14, so Wanjiku's 96 stops at 100.

## When you're stuck

- **`ERROR 1304: PROCEDURE AddBonus already exists`**: `DROP PROCEDURE IF EXISTS` first.
- **`ERROR 1064` near `END`**: the `DELIMITER //` lines are missing.
- **`AddBonus` makes the project twice**: insert the project only `WHERE NOT EXISTS`, then look its id up by name.
- **`ERROR 1318: Incorrect number of arguments for PROCEDURE`**: count the parameters in your `CREATE` and in the `CALL`.
- **`@n` is `NULL`**: the parameter must be `OUT`, and the `SELECT ... INTO` must name it.
- **`RenameProject` renames every project**: the `WHERE` compared the column with itself. Check your parameter names.
- **`ERROR 1337: Variable or condition declaration after cursor or handler declaration`**, or `1064` on a `DECLARE`: `DECLARE`s go first in the block, before any other statement.
