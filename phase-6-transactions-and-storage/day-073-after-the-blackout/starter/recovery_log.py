"""Day 73: logs, undo, redo and checkpoints.

A log is a list of records, oldest first:
    ("start", T)
    ("update", T, item, old, new)    T changed item from old to new
    ("commit", T)
    ("abort", T)                     T was rolled back before the crash, and its changes were undone
    ("checkpoint", (T, ...))         everything before this is on disk; these transactions were still running

`disk` is a dict item -> value: what was on disk when the power went. Never change the dict you're given;
return a new one.
"""


def losers(log):
    """Transactions that started but have no commit or abort record: the ones the crash caught mid-way.
    Sorted."""
    raise NotImplementedError("write this")


def undo_recover(log, disk):
    """Undo logging: a transaction's changes may reach disk before it commits, and its commit record is written
    only after all of them have. Recovery: go backwards through the log and put back the old value of every
    update by a loser."""
    raise NotImplementedError("write this")


def redo_recover(log, disk):
    """Redo logging: nothing reaches disk until the transaction's commit record is in the log. Recovery: go
    forwards and write the new value of every update by a committed transaction."""
    raise NotImplementedError("write this")


def undo_redo_recover(log, disk):
    """Undo/redo logging (what InnoDB and most real systems do): any change can be on disk or not, committed
    or not. Recovery: redo every committed transaction's updates going forwards, then undo every update by a
    transaction that didn't commit, going backwards."""
    raise NotImplementedError("write this")


def scan_from(log):
    """The index of the oldest record undo/redo recovery has to read. No checkpoint: 0. Otherwise the last
    checkpoint, or the start record of a transaction it lists that never finished, whichever is earlier."""
    raise NotImplementedError("write this")


def follows_wal(events):
    """Kata: check the write-ahead logging rules for undo/redo logging. Events, in order:
        ("log", record)    a record goes into the log buffer in memory
        ("flush",)         the whole log buffer is written to the log on disk
        ("write", item)    item's page is written to disk
        ("tell", T)        the customer is told T committed
    A page may be written only once every logged update to that item is on disk; a customer may be told only
    once T's commit record is on disk. Return the index of the first event that breaks a rule, or None."""
    raise NotImplementedError("write this")
