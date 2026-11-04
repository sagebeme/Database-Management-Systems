"""Day 68: can we undo it? Recoverable, cascadeless and strict schedules.

A schedule is a list of Op(kind, txn, item) from coursekit.schedules.parse. An aborted transaction's writes are
undone, so after a1, a read of an item T1 wrote sees whatever was there before T1's write.
"""

from coursekit.schedules import parse  # noqa: F401


def reads_from(schedule):
    """Every time a transaction reads a value written by ANOTHER transaction: (reader, writer, item), in order.
    The writer is the last transaction to write the item before the read, not counting writes undone by an
    abort. Reading your own write, or the initial value, isn't reading from anyone."""
    raise NotImplementedError("write this")


def is_recoverable(schedule):
    """Whenever Ti reads from Tj and Ti commits, Tj has committed before Ti's commit."""
    raise NotImplementedError("write this")


def is_cascadeless(schedule):
    """Every read from another transaction happens after that writer has committed."""
    raise NotImplementedError("write this")


def is_strict(schedule):
    """No transaction reads or writes an item that another transaction has written, until that writer has
    committed or aborted."""
    raise NotImplementedError("write this")


def cascade(schedule, aborting):
    """If `aborting` aborts, every transaction that read a value it wrote must abort too, and every one that
    read from those, and so on. Return them, sorted (not including `aborting`)."""
    raise NotImplementedError("write this")


def classify(schedule):
    """Kata: the strongest that holds: "strict", "cascadeless", "recoverable" or "not recoverable"."""
    raise NotImplementedError("write this")
