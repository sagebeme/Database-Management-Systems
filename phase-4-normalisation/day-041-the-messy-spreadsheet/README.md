# Day 41: The Messy Spreadsheet

## The brief

Elimu Tuition Centre in Eldoret keeps its registrations in one spreadsheet, now a single MySQL table. Each row has a student and their phone, a subject and its fee, and the subject's tutor and the tutor's room. The director, Mrs Jeptoo, has three complaints:

- Mr Omondi moved rooms, and somebody updated two of his three rows.
- She wants to advertise Geography, with a new tutor, but there's nowhere to put it until a student registers.
- Cynthia is the only Biology student. If she leaves, the centre forgets the Biology fee and who teaches it.

Day 15 called these the update, insert and delete **anomalies**. Phase 4 is about finding them *before* the data goes in, with a precise test for "this table stores a fact more than once". Today you meet the problem again, measure it, fix it by hand, and prove the fix loses nothing. Tomorrow starts the theory that tells you how to split a table without guessing.

## What you'll use

```
registrations_flat
+---------------+--------------+-----------+------+------------+------------+
| student       | student_phone| subject   | fee  | tutor      | tutor_room |
+---------------+--------------+-----------+------+------------+------------+
| Amani Kiptoo  | 254711000001 | Maths     | 3000 | Mr Omondi  | R1         |
| Baraka Said   | 254722000002 | Maths     | 3000 | Mr Omondi  | R1         |  <- Maths's fee, tutor and
| Cynthia Njoki | 254733000003 | Maths     | 3000 | Mr Omondi  | R1         |     room, three times over
...
```

The key is `(student, subject)`. But look at what depends on what:

- `student → student_phone`: the phone depends on the student only, not the subject.
- `subject → fee, tutor`: the fee and tutor depend on the subject only.
- `tutor → tutor_room`: the room depends on the tutor, and only through the subject on the key.

Each of those facts is repeated in every row that mentions it, which is what causes all three anomalies. The fix is a table per fact:

```
tutors (name, room)                     subjects (name, fee, tutor -> tutors)
students (name, phone)                  registrations (student -> students, subject -> subjects)
```

**A split must be lossless**: joining the parts back must give exactly the original rows, no more and no fewer (Day 46 makes this precise). You'll check it by rebuilding the spreadsheet with joins.

`INSERT INTO t SELECT DISTINCT ...` fills a new table from the old one, each fact once.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS tuition;"
tools/mysql.sh tuition < phase-4-normalisation/day-041-the-messy-spreadsheet/setup.sql
```

1. `starter/0-rows_for_one_fact.sql`: how many rows record Mr Omondi's room? Column `rows`. (`ROWS` is a reserved word in MySQL 8: write it as `` `rows` ``.)
2. `starter/1-omondi_moves.sql`: he moves to R5. Update every row that says otherwise.
3. `starter/2-split.sql`: create `tutors` (`name` PK, `room`), `subjects` (`name` PK, `fee`, `tutor` → `tutors`), `students` (`name` PK, `phone` unique) and `registrations` (`student` → `students`, `subject` → `subjects`, the pair as the key), then fill them from `registrations_flat`.
4. `starter/3-add_geography.sql`: in the split design, add Geography (2800) taught by Mr Barasa in R6. No student needed.
5. `starter/4-rebuild.sql`: join the split tables back into the spreadsheet's six columns, ordered by student and subject. The test compares it with the original, row for row.
6. `starter/answers.py`: name each anomaly.
7. `pytest phase-4-normalisation/day-041-the-messy-spreadsheet`

## The kata: Fee Rise

In `starter/kata.sql`, raise the Physics fee by 10% (to whole shillings) in the split design. One row changes; in the spreadsheet, it would have been two.

## When you're stuck

- **`ERROR 1064` near `rows`**: `ROWS` is reserved. Quote the alias with backticks.
- **`2-split.sql` fails on the subjects insert with a foreign key error**: create and fill `tutors` before `subjects`, and `students` and `subjects` before `registrations`.
- **`Duplicate entry 'Maths' for key 'subjects.PRIMARY'`**: use `SELECT DISTINCT`.
- **The rebuild has extra rows**: join `subjects` to `tutors` on the tutor's name, and `registrations` to both other tables. A missing `ON` condition makes a cross join.
- **The kata changes every fee**: the `UPDATE` needs `WHERE name = 'Physics'`.
