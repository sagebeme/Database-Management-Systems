# Day 56: Who Reports to Whom

## The brief

Ziwani County's HR office keeps one table, `employees`, where each person points at their manager (`manager_id`), the self-join from Day 34. A self-join answers "who is Brian's manager?" One level. But HR's real questions go all the way up or down:

- Who is in Brian's chain of command, right up to the Governor?
- Draw the whole org chart.
- How many people does each director have under them, at every level?
- Who's the closest boss two people share (for a complaint between them)?

You don't know how many levels there are, so you can't write the right number of joins. A **recursive CTE** keeps joining until there's nothing left.

## What you'll use

**A CTE** (common table expression) names a query so the rest of the statement can use it, like a derived table you write first:

```sql
WITH averages AS (
    SELECT department, AVG(salary) AS dept_avg FROM employees GROUP BY department
)
SELECT e.name, a.dept_avg FROM employees AS e JOIN averages AS a ON a.department = e.department;
```

You can have several (`WITH a AS (...), b AS (...)`), and a later one can use an earlier one.

**A recursive CTE** has two parts joined by `UNION ALL`:

```sql
WITH RECURSIVE chain AS (
    SELECT id, name, manager_id, 0 AS level          -- the anchor: where to start
    FROM employees WHERE name = 'Brian Kiprono'
    UNION ALL
    SELECT e.id, e.name, e.manager_id, c.level + 1   -- the step: uses the rows found last time
    FROM employees AS e JOIN chain AS c ON e.id = c.manager_id
)
SELECT * FROM chain;
```

MySQL runs the anchor, then the step on the anchor's rows, then the step on *those* rows, until a step finds nothing.

- **Going up** (to the boss): join `e.id = c.manager_id`. **Going down** (to the team): `e.manager_id = c.id`.
- **Column types come from the anchor.** If the anchor's `path` is just `name` (`VARCHAR(60)`), the longer paths built later don't fit: `ERROR 1406: Data too long for column 'path'`. Make room in the anchor: `CAST(name AS CHAR(1000)) AS path`.
- **Runaway recursion stops** at `cte_max_recursion_depth` (1000 by default) with `ERROR 3636`. That's a sign of a loop in the data, or a step with no way to stop.
- **Generating rows**: a recursive CTE doesn't need a table at all. `SELECT 1 UNION ALL SELECT n + 1 FROM nums WHERE n < 10` counts to 10. The same idea with `day + INTERVAL 1 DAY` gives every date in a range, and a `LEFT JOIN` then shows the days with no sales.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS county;"
tools/mysql.sh county < phase-5-advanced-mysql/day-056-who-reports-to-whom/setup.sql
```

1. `starter/0-above_average.sql`: a plain CTE (the tests check you used `WITH`).
2. `starter/1-chain_of_command.sql`: Brian Kiprono up to the top.
3. `starter/2-org_chart.sql`: everyone, with depth and path.
4. `starter/3-team_size.sql`: how many people sit under each manager. Hint: first make every (boss, person) pair at any depth.
5. `starter/4-every_day.sql`: every date in the takings range, closed days as 0.
6. `pytest phase-5-advanced-mysql/day-056-who-reports-to-whom`

## The kata: Lowest Common Boss

In `starter/kata.sql`, find the closest person that both Brian Kiprono and Samuel Mutua report to. If one of them is above the other, it's that person. Walk both chains up, keep the people in both, and take the one fewest steps from Brian.

## When you're stuck

- **`ERROR 1406: Data too long for column 'path' at row 1`**: cast the anchor's path to a longer type.
- **`ERROR 3636: Recursive query aborted after 1001 iterations`**: the step never stops. Check its join goes one way (up *or* down), and the date series has a `WHERE day < ...`.
- **The chain starts at the Governor and has one row**: your anchor is `WHERE manager_id IS NULL` (the top). For a chain *up* from Brian, start at Brian.
- **The team sizes are all 1**: you counted direct reports only. Build (boss, person) pairs, then add (the boss's boss, person) in the step.
- **The kata says Amina Hassan**: she's a common boss, just not the lowest. Order by the number of steps from Brian and take the first.
