# Day 72: Who Came First

## The brief

Locks make transactions wait, and waiting brings deadlocks (Day 71). There's another way: give every transaction a **timestamp** when it starts, and promise that the result will be the same as running them one at a time *in timestamp order*. Nobody waits. When a transaction tries something that would break the promise (reading a value a younger transaction already overwrote, say) it's rolled back.

Think of a busy M-Pesa agent's queue: everyone gets a number at the door, and the agent's float must end up as if customers were served strictly by number. If customer 7 tries to change something customer 9 has already looked at, customer 7 goes to the back.

Today you'll run schedules through **basic timestamp ordering** and the **Thomas write rule**, then use timestamps the other way: to decide who waits and who dies when locks clash.

## What you'll use

Every item keeps two numbers, both 0 at the start:

- **RTS(X)**: the largest timestamp that has read X.
- **WTS(X)**: the largest timestamp that has written X.

**Basic timestamp ordering**, for a transaction with timestamp `ts`:

| Operation | Too late if | Otherwise |
|---|---|---|
| read X | `ts < WTS(X)`: a younger transaction already overwrote what it should have seen | `RTS(X) = max(RTS(X), ts)` |
| write X | `ts < RTS(X)`: a younger one already read the old value; or `ts < WTS(X)`: a younger one already wrote | `WTS(X) = ts` |

"Too late" means roll the transaction back. Nobody ever waits, so there are **no deadlocks**, and the schedules it allows are conflict serializable (in timestamp order). It doesn't stop a transaction reading uncommitted data, though, so on its own it isn't recoverable; real systems add a commit check.

**The Thomas write rule** changes one thing. A write with `ts < WTS(X)` (but `ts >= RTS(X)`) is simply **ignored**: a younger transaction has already written X, and in timestamp order this older write would have been overwritten anyway, with nobody reading it in between. The transaction carries on. That lets through schedules that are view serializable but not conflict serializable (Day 70's blind writes).

**Restarting**: a rolled-back transaction usually starts again with a *new* timestamp under timestamp ordering. Today it just stops.

**Timestamps for locking.** With locks, timestamps can decide who waits, so a waits-for cycle can never form:

| `requester` wants a lock `holder` has | requester is older | requester is younger |
|---|---|---|
| **Wait-die** | waits | dies (rolls back) |
| **Wound-wait** | wounds the holder (holder rolls back) | waits |

In wait-die only an *older* transaction waits for a younger one; in wound-wait only a *younger* one waits for an older one. Either way every waiting edge points the same direction, so there's no cycle. A restarted transaction **keeps its old timestamp**, so it gets older and eventually can't lose: no starvation.

InnoDB doesn't do any of this: it uses locks plus deadlock detection (Day 71). Timestamps show up in multiversion schemes, distributed databases (Spanner, CockroachDB) and the textbook exam questions you'll meet.

## Steps

Pure Python today.

1. `starter/timestamps.py`: `default_timestamps`, `basic_to`, `thomas_write_rule` (or the shared `_run`), `aborted`, `wait_die`, `wound_wait`.
2. `starter/answers.py`.
3. `pytest phase-6-transactions-and-storage/day-072-who-came-first`

Work a few schedules on paper first, with an RTS/WTS table for each item. For `r1(A) w2(A) c2 w1(A) c1`:

| op | T's ts | A's RTS, WTS before | outcome |
|---|---|---|---|
| r1(A) | 1 | 0, 0 | ok, RTS = 1 |
| w2(A) | 2 | 1, 0 | ok, WTS = 2 |
| c2 | | | ok |
| w1(A) | 1 | 1, 2 | `1 < WTS`: abort (basic) or ignore (Thomas) |
| c1 | | | skip (basic) or ok (Thomas) |

## The kata: Fewest Aborts

In `starter/timestamps.py`, write `fewest_aborts(schedule)`: try every way of handing out timestamps, run basic timestamp ordering with each, and return `(order, aborts)` for the order that rolls back the fewest transactions. Ties go to the smallest tuple. When the best is 0, the order you find is a serial order the schedule is conflict-equivalent to.

## When you're stuck

- **Everything is "ok"**: compare timestamps, not positions in the schedule. With the default timestamps, the transaction that appears first is the oldest.
- **A transaction aborts on reading its own write**: `ts < WTS` is strict; reading what you wrote yourself has `ts == WTS`.
- **The test about aborted writes fails**: don't undo RTS or WTS when a transaction rolls back. (Real systems would; it makes paper exercises messy, so ours don't.)
- **Thomas ignores a write that should abort**: check `ts < RTS` *first*. A younger transaction that read the old value can't be fixed by ignoring.
- **`wait_die` and `wound_wait` are swapped**: in both, the *older* transaction gets its way. Wait-die: the older waits patiently, the younger dies. Wound-wait: the older wounds, the younger waits.
