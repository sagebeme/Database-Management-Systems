# Day 29: The Exercise Book Problem

## The brief

Before the Tumaini chama got a database, Mama Wanjiku kept the records in an exercise book: members on one page, contributions on another. Then her nephew typed them into two CSV files and wrote a few Python functions to work with them. It worked, for a while.

Today you write those functions yourself. Each one makes you do by hand a job that a database does for you, and you'll feel how fragile each is. Phase 3 is about *designing* databases, and it starts with why we bother with a database at all.

```
members.csv               contributions.csv
id,name,phone             member_id,month,amount
1,Wanjiku,254711000001    1,2026-09,1000
2,Otieno,254722000002     2,2026-09,1000
3,Chebet,254733000003     7,2026-10,500     <- member 7 doesn't exist
```

## What you'll use

Python's `csv` module (`csv.DictReader` and `csv.DictWriter`) and `os.replace`. `read_rows` is written for you.

The classic list of problems with keeping data in plain files, and what a DBMS gives you instead:

| Problem with files | What goes wrong | What a DBMS gives you | Where in this course |
|---|---|---|---|
| Redundancy and inconsistency | the same fact in many files, disagreeing | one fact in one place | Days 15, 41–52 |
| Hard to ask new questions | every question is a new program | a query language | Phase 1 |
| Integrity | rules (unique phones, real member ids) checked by every program, or by none | constraints, checked always | Days 16, 17, 31, 53 |
| Atomicity | a crash halfway leaves a half-written file | transactions and a recovery log | Days 65, 73 |
| Concurrent access | two people writing at once overwrite each other | locking and isolation | Days 66–72 |
| Security | anyone who can open the file can read all of it | users and privileges | Day 25 |
| Data isolation | data scattered in different formats | one schema, one engine | Day 35 |

A DBMS also separates *what* the data means (the schema) from *how* it's stored on disk, so programs don't break when storage changes. That's **data independence**, and it's why your SQL from Phase 1 would still work if MySQL changed its file format tomorrow.

## Steps

Fill in the functions in `starter/book.py`. The docstrings say exactly what each must do.

1. `add_member`: the next id, the header row for a new file, and a `ValueError` for a phone that's already taken. You're writing a `UNIQUE` constraint and `AUTO_INCREMENT` by hand.
2. `find_by_phone`: a full scan of the file. A database would use an index (Day 62).
3. `totals`: each member's total, 0 for those who haven't paid. That's a `LEFT JOIN` with `GROUP BY`, by hand.
4. `orphans`: contributions by members who don't exist. A `FOREIGN KEY` would have refused them.
5. `rename`: change one name by rewriting the file, safely: write a temporary file, then `os.replace` it over the original (an atomic swap on the same disk).
6. `pytest phase-3-design/day-029-the-exercise-book-problem`

## The kata: Two Treasurers

In `starter/book.py`, write `add_member_locked`. The test starts 16 threads adding members at the same instant. Without a lock, two of them read the file at the same moment, both decide the next id is 5, and both write it. Hold an exclusive `fcntl.flock` on `members.csv.lock` while you read and write. (`fcntl` exists on Linux and macOS; on Windows, use WSL.)

Once it passes, think about what you just built: a lock, so that only one writer runs at a time. Every serious database does this, at a much finer grain (Day 71).

## When you're stuck

- **The new file has no header**: check whether the file exists *before* you open it for appending.
- **`totals` is missing Chebet**: start every member at 0 before adding contributions.
- **`orphans` returns everything**: ids from `csv` are strings. Compare `"7"` with `"7"`, not with `7`.
- **`rename` loses rows**: write *every* row back, not only the changed one.
- **The kata gives duplicate ids only sometimes**: that's a race. The lock must cover both the read (finding the biggest id) and the write.
