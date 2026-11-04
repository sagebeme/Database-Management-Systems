# Day 66: Two Tellers, One Account

## The brief

Wanjiku's SACCO account holds 1,500. At 9:00:00 two tellers, in two branches, each pay her 100 at the same moment. Each teller's system reads the balance (1,500), checks there's enough, and writes 1,400. Both write 1,400. She received 200 and the account shows 100 gone. One update has been **lost**, and nobody saw an error.

Yesterday's transactions made one change all-or-nothing. Today is about **many transactions at the same time**: what goes wrong when they overlap, how to name each problem, and two ways to fix the lost update for real, with 20 tellers racing.

## What you'll use

**The anomalies**, in schedule notation (`r1(A)` is T1 reading A, `w2(A)` is T2 writing it, `c1` and `a1` are commit and abort; see `tools/coursekit/schedules.py`):

| Anomaly | Pattern | What goes wrong |
|---|---|---|
| **Dirty read** | `w1(A) r2(A) a1` | T2 read a value that never officially existed |
| **Non-repeatable read** | `r1(A) w2(A) c2 r1(A)` | T1 reads A twice and gets two answers |
| **Lost update** | `r1(A) r2(A) w2(A) w1(A)` | T1 writes a value worked out before T2's write, wiping it out |
| **Phantom** | T1 counts the trip's bookings, T2 inserts one, T1 counts again | a *row* appears that wasn't there; no single row was changed |

**Fixing the lost update:**

1. **Check and change in one statement.** `UPDATE accounts SET balance = balance - 100 WHERE phone = ? AND balance >= 100` reads and writes inside the database, row-locked, in one step. Then ask how many rows changed: 1 means it worked, 0 means there wasn't enough.
2. **Lock what you read**, when you must read first (to show the customer, or for a calculation too complex for one statement):

   ```sql
   START TRANSACTION;
   SELECT balance FROM accounts WHERE phone = ? FOR UPDATE;   -- others wait here until we commit
   UPDATE accounts SET balance = ? WHERE phone = ?;
   COMMIT;
   ```

   `FOR UPDATE` takes an exclusive lock on the rows it reads, until the transaction ends (Day 71).

**Phantoms** can't be fixed by locking rows you've read, because the new row didn't exist when you read. Lock something they all share instead, such as the parent row (the trip), or use `SERIALIZABLE` (Day 67).

**From Python**: each thread needs its *own* connection. PyMySQL connections aren't safe to share between threads. The tests start them all at once with a `threading.Barrier`.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS sacco;"
tools/mysql.sh sacco < phase-6-transactions-and-storage/day-066-two-tellers-one-account/setup.sql
```

1. Read `withdraw_unsafe` in `starter/tellers.py` (done for you). Its test shows it losing money.
2. `withdraw_atomic`: one statement.
3. `withdraw_locked`: read with `FOR UPDATE`, `pause()`, write, commit.
4. `starter/anomalies.py`: `dirty_reads`, `non_repeatable_reads`, `lost_updates` on paper schedules.
5. `starter/answers.py`.
6. `pytest phase-6-transactions-and-storage/day-066-two-tellers-one-account`

## The kata: Double Booking

In `starter/booking.py`, write `book_seat(conn, trip_id, passenger, pause)`. The Machakos matatu has 2 seats left and 6 people tap "book" at once. Counting the bookings and then inserting one is a phantom waiting to happen. Lock the trip's row first, so the bookings for one trip happen one at a time.

## When you're stuck

- **`withdraw_locked` still loses money**: `FOR UPDATE` only locks inside a transaction. With autocommit on, a lone `SELECT ... FOR UPDATE` releases its lock straight away. `START TRANSACTION` first.
- **The tests hang, then fail with `Lock wait timeout exceeded` (1205)**: a transaction was never committed or rolled back. The early `return False` needs a `conn.rollback()` too.
- **`withdraw_atomic` returns `True` when it shouldn't**: `cursor.execute` returns the number of rows changed. Compare it with 1.
- **`dirty_reads` flags `w1(A) r1(A)`**: reading your own write isn't dirty. Skip `j == i`.
- **`lost_updates` flags `r1(A) w2(A) r1(A) w1(A)`**: T1 read again after T2's write, so its write is based on fresh data. Forget the older read when Ti reads again.
- **The kata books 3 or more**: you locked nothing, or locked the bookings you counted (the new row isn't among them). Lock `trips` with `FOR UPDATE`.
