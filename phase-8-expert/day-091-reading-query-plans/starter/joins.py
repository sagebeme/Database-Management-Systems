"""Day 91: the three join algorithms, by hand.

A relation is a list of dicts. Join r and s on `key` (a column both have): every pair of rows with equal keys,
merged into one dict ({**r_row, **s_row}). Rows with a None key never match.
Each function returns (rows, work): the joined rows, and a count of the work done, as each docstring says.
"""

import math


def nested_loop_join(r, s, key):
    """For each row of r, look at every row of s. work = the number of key comparisons (len(r) * len(s))."""
    raise NotImplementedError("write this")


def hash_join(r, s, key):
    """Build a dict from s's key to its rows, then probe it with each row of r. work = len(s) (building) +
    len(r) (probing)."""
    raise NotImplementedError("write this")


def block_nested_loop_cost(r_blocks, s_blocks, buffers):
    """Block reads for a block nested-loop join with r as the outer relation and `buffers` pages of memory: one
    page for s, one for the output, the rest for chunks of r. r_blocks + ceil(r_blocks / (buffers - 2)) * s_blocks."""
    raise NotImplementedError("write this")


def sort_merge_join(r, s, key):
    """Kata: sort both on key, then walk them together. A key that appears several times on both sides joins
    every r row with every s row for it. work = the number of times you move forward in r or s while merging
    (not counting the sorting)."""
    raise NotImplementedError("write this")
