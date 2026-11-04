"""Day 91: the three join algorithms, by hand.

A relation is a list of dicts. Join r and s on `key` (a column both have): every pair of rows with equal keys,
merged into one dict ({**r_row, **s_row}). Rows with a None key never match.
Each function returns (rows, work): the joined rows, and a count of the work done, as each docstring says.
"""

import math


def nested_loop_join(r, s, key):
    """For each row of r, look at every row of s. work = the number of key comparisons (len(r) * len(s))."""
    rows, work = [], 0
    for a in r:
        for b in s:
            work += 1
            if a[key] is not None and a[key] == b[key]:
                rows.append({**a, **b})
    return rows, work


def hash_join(r, s, key):
    """Build a dict from s's key to its rows, then probe it with each row of r. work = len(s) (building) +
    len(r) (probing)."""
    table = {}
    for b in s:
        if b[key] is not None:
            table.setdefault(b[key], []).append(b)
    rows = [{**a, **b} for a in r for b in table.get(a[key], [])]
    return rows, len(s) + len(r)


def block_nested_loop_cost(r_blocks, s_blocks, buffers):
    """Block reads for a block nested-loop join with r as the outer relation and `buffers` pages of memory: one
    page for s, one for the output, the rest for chunks of r. r_blocks + ceil(r_blocks / (buffers - 2)) * s_blocks."""
    return r_blocks + math.ceil(r_blocks / (buffers - 2)) * s_blocks


def sort_merge_join(r, s, key):
    """Kata: sort both on key, then walk them together. A key that appears several times on both sides joins
    every r row with every s row for it. work = the number of times you move forward in r or s while merging
    (not counting the sorting)."""
    r = sorted((a for a in r if a[key] is not None), key=lambda a: a[key])
    s = sorted((b for b in s if b[key] is not None), key=lambda b: b[key])
    rows, work, i, j = [], 0, 0, 0
    while i < len(r) and j < len(s):
        if r[i][key] < s[j][key]:
            i += 1
            work += 1
        elif r[i][key] > s[j][key]:
            j += 1
            work += 1
        else:
            k = r[i][key]
            i2 = i
            while i2 < len(r) and r[i2][key] == k:
                i2 += 1
            j2 = j
            while j2 < len(s) and s[j2][key] == k:
                j2 += 1
            rows += [{**a, **b} for a in r[i:i2] for b in s[j:j2]]
            work += (i2 - i) + (j2 - j)
            i, j = i2, j2
    return rows, work
