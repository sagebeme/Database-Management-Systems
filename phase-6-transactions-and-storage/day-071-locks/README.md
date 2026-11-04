# Day 71: Locks

## The brief

Days 69 and 70 *checked* whether a finished schedule was safe. A real database can't wait until the end to find out: it has to stop bad interleavings while they're happening. Most do it with **locks**. Before touching a row, a transaction takes a lock on it, and anyone who wants a conflicting lock waits.

Locks bring their own problem. Two Kenyan SACCO members send each other money at the same moment: one transfer locks account A and waits for B, the other locks B and waits for A. Neither can ever go on. That's a **deadlock**, and today you'll make MySQL produce one, watch it pick a victim, and then write transfers that can't deadlock at all.

## What you'll use

**Lock modes**: shared (S) for reading, exclusive (X) for writing. Only S with S is compatible.

| held \ wanted | S | X |
|---|---|---|
| S | ✓ | wait |
| X | wait | wait |

In schedules: `sl1(A)` (T1 takes a shared lock on A), `xl1(A)` (exclusive), `u1(A)` (unlock). A transaction holding S on A can **upgrade** to X if nobody else holds a lock on A.

**Two-phase locking (2PL)**: each transaction has a *growing* phase (taking locks) and then a *shrinking* phase (releasing them). Once it unlocks anything, it never locks again. 2PL guarantees conflict serializability, but not freedom from deadlocks or cascading aborts.

- **Strict 2PL**: exclusive locks are held until commit or abort, so nobody reads uncommitted data. That makes schedules strict (Day 68).
- **Rigorous 2PL**: *every* lock is held until commit. That's what InnoDB does with the locks it takes.
- **Conservative (static) 2PL**: a transaction takes *all* its locks before it does anything, or none and tries again later. A transaction holding locks never waits for one, so no deadlock can form. The catch: it must know every item it will touch in advance, which real transactions rarely do. GATE asks about it; real databases don't use it.

So: basic 2PL gives serializability; strict 2PL adds no cascading aborts; rigorous 2PL is stricter still; conservative 2PL alone rules out deadlocks.

**In MySQL**: `UPDATE` and `DELETE` take exclusive row locks. `SELECT ... FOR UPDATE` takes exclusive locks on the rows it reads, and `SELECT ... FOR SHARE` shared ones. A plain `SELECT` takes none: it reads a snapshot (Day 67).

**Deadlocks**: in the **waits-for graph**, Ti → Tj when Ti waits for a lock Tj holds. A cycle is a deadlock. InnoDB checks for cycles as locks are requested, picks a **victim**, rolls it back, and gives it `ERROR 1213: Deadlock found when trying to get lock; try restarting transaction`. Two cures, and real systems use both:

1. **Prevent it**: everyone takes locks in the same order, for example the smaller account number first. Then no cycle can form.
2. **Retry**: catch 1213, roll back, and run the whole transaction again.

## Steps

```bash
tools/mysql.sh -e "CREATE DATABASE IF NOT EXISTS locks;"
tools/mysql.sh locks < phase-6-transactions-and-storage/day-071-locks/setup.sql
```

Make a deadlock by hand, in two terminals: `START TRANSACTION; SELECT * FROM accounts WHERE phone = '254711000001' FOR UPDATE;` in the first, the same with `'254722000002'` in the second. Then each asks for the *other* row `FOR UPDATE`.

1. `starter/locks.py`: `is_well_formed`, `follows_2pl`, `follows_strict_2pl` and `deadlocked`.
2. `starter/transfers.py`: `transfer_naive` is done for you, and its test shows it deadlocking. Write `transfer_ordered` and `transfer_with_retry`.
3. `starter/answers.py`.
4. `pytest phase-6-transactions-and-storage/day-071-locks`

## The kata: Could Locks Have Made This?

In `starter/locks.py`, write `possible_under_rigorous_2pl(schedule)`: given a schedule with no lock operations, could rigorous 2PL have produced it? Add the locks as late as possible (S just before a transaction's first read of an item, X just before its first write, upgrading from S), let commits release everything, and check the result with `is_well_formed`.

## When you're stuck

- **`is_well_formed` allows `sl1(A) sl2(A) xl1(A)`**: an upgrade needs *nobody else* holding any lock on the item.
- **`is_well_formed` rejects reads after an upgrade**: an X lock covers reads too.
- **`follows_strict_2pl` passes `xl1(A) w1(A) u1(A) ... c1`**: unlocking an exclusive lock before the commit breaks strictness, even if 2PL holds.
- **`deadlocked` reports two readers waiting on each other's shared locks**: S doesn't block S. Someone has to *want* or *hold* an X.
- **`transfer_ordered` still deadlocks**: sort the two phones and lock the smaller one first, whichever is the sender.
- **`transfer_with_retry` says `Commands out of sync`, or waits forever**: after a 1213, call `conn.rollback()` before trying again.
