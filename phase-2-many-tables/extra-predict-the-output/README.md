# Extra: Predict the Output

This drill sits after Day 28, outside the hundred days. Do it at the end of Phase 2, and again before an exam or an interview.

## The brief

GATE and interviewers love one kind of SQL question: here are the tables, here's a query, what comes back? Answering it means knowing what the database does, not what you'd guess it does, and the traps are always the same few: `NULL`, empty subqueries, duplicates, and where a condition sits in an outer join.

Seventeen queries on one small table. Work out each answer **on paper, without running anything**. Then type your predictions into `starter/answers.py` and let the tests mark them. Only after that, load the data and run the queries to see where you went wrong.

## What you'll use

```
departments (name, floor)          staff (id, name, dept, salary)
 Sales    1                          1 Achieng  Sales    40000
 Tech     2                          2 Baraka   Sales    55000
 Finance  3                          3 Chebet   Sales    NULL
 Legal    4                          4 Daudi    Tech     90000
                                     5 Esther   Tech     70000
                                     6 Faraji   Tech     70000
                                     7 Gathoni  Finance  60000
                                     8 Hamisi   NULL     30000
                                     9 Imani    Finance  NULL
```

Everything from Phases 1 and 2, plus one thing the days didn't cover: **comparing with every row of a subquery**.

```sql
salary > ALL (SELECT ...)   -- bigger than every value the subquery returns
salary > ANY (SELECT ...)   -- bigger than at least one of them (SOME means the same as ANY)
```

- `= ANY (...)` is the same as `IN (...)`, and `<> ALL (...)` is the same as `NOT IN (...)`.
- **`ALL` over an empty subquery is true**, for every row, even a row whose own value is `NULL`. There's nothing to be smaller than. `ANY` over an empty subquery is false.
- **A `NULL` in the subquery poisons `ALL`.** `x > ALL (40000, 55000, NULL)` asks whether `x > NULL` too, which is unknown, so the result is never true. It's the `NOT IN` trap from Day 22 in another form.
- `x > ALL (...)` is `x > MAX(...)`, and `x > ANY (...)` is `x > MIN(...)`, *except* for those two edge cases. That's exactly why exams ask about them.

## Steps

Each answer is a number (a count of rows, or a value), except Q12, which is a name. "How many rows" means how many rows the query returns.

**Q1**. `SELECT COUNT(*) FROM staff WHERE salary > ALL (SELECT salary FROM staff WHERE dept = 'Sales');`

**Q2**. `SELECT COUNT(*) FROM staff WHERE salary > ALL (SELECT salary FROM staff WHERE dept = 'Legal');`

**Q3**. `SELECT COUNT(*) FROM staff WHERE salary > ANY (SELECT salary FROM staff WHERE dept = 'Sales');`

**Q4**. `SELECT COUNT(*) FROM staff WHERE salary >= ALL (SELECT salary FROM staff WHERE dept = 'Tech');`

**Q5**. `SELECT COUNT(*) FROM departments WHERE name <> ALL (SELECT dept FROM staff);`

**Q6**. `SELECT COUNT(*) FROM departments d WHERE NOT EXISTS (SELECT 1 FROM staff s WHERE s.dept = d.name);`

**Q7**. `SELECT COUNT(DISTINCT salary) FROM staff;`

**Q8**. How many rows: `SELECT dept, COUNT(*) FROM staff GROUP BY dept;`

**Q9**. `SELECT AVG(salary) FROM staff WHERE dept = 'Sales';` (as a whole number)

**Q10**. `SELECT COUNT(*) FROM departments d LEFT JOIN staff s ON s.dept = d.name AND s.salary > 50000;`

**Q11**. `SELECT COUNT(*) FROM departments d LEFT JOIN staff s ON s.dept = d.name WHERE s.salary > 50000;`

**Q12**. In MySQL: `SELECT name FROM staff ORDER BY salary, name LIMIT 1;`

**Q13**. How many rows: `SELECT dept FROM staff UNION SELECT name FROM departments;`

**Q14**. `SELECT COUNT(*) FROM staff s WHERE salary > (SELECT AVG(salary) FROM staff t WHERE t.dept = s.dept);`

**Q15**. `SELECT COUNT(*) FROM staff a JOIN staff b ON a.salary = b.salary AND a.id <> b.id;`

**Q16**. How many rows: `SELECT COUNT(*) FROM staff HAVING COUNT(*) > 100;`

**Q17**. How many rows: `SELECT DISTINCT dept FROM staff;`

Mark yourself:

```bash
pytest phase-2-many-tables/extra-predict-the-output
```

Then check the ones you missed by running them:

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS drill;"
tools/mysql.sh drill < phase-2-many-tables/extra-predict-the-output/setup.sql
tools/mysql.sh drill -e "SELECT COUNT(*) FROM staff WHERE salary > ALL (SELECT salary FROM staff WHERE dept = 'Sales');"
```

## When you're stuck

Only after marking:

- **Q1, Q5**: a `NULL` in the subquery. Chebet's salary is in Q1's list, Hamisi's missing department in Q5's.
- **Q2**: Legal has nobody, so the subquery is empty.
- **Q6 vs Q5**: `NOT EXISTS` doesn't care about `NULL`s; `<> ALL` (`NOT IN`) does. Day 22.
- **Q7, Q9**: aggregates skip `NULL`s, so `AVG` divides by 2, not 3.
- **Q8, Q17**: `GROUP BY` and `DISTINCT` put all the `NULL`s together into one group. `COUNT(DISTINCT dept)` would skip it.
- **Q10 vs Q11**: a condition on the right table in `ON` keeps every department; in `WHERE` it throws away the padded rows. Day 20.
- **Q12**: MySQL sorts `NULL` first in ascending order. PostgreSQL sorts it last.
- **Q14**: Hamisi has no department, so his subquery averages nothing and returns `NULL`.
- **Q16**: with no `GROUP BY` the whole table is one group, and `HAVING` can remove it, leaving no rows at all.
