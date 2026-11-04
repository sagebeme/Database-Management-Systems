"""Day 74: blocks, blocking factors and what a lookup costs.

Sizes are in bytes. Records don't span blocks (a record that doesn't fit in what's left of a block starts the
next one). Costs are counted in block reads: the disk is so much slower than memory that nothing else matters.
"""

import math


def blocking_factor(block_size, record_size):
    """How many whole records fit in one block (bfr)."""
    raise NotImplementedError("write this")


def file_blocks(records, bfr):
    """How many blocks `records` records take, `bfr` to a block."""
    raise NotImplementedError("write this")


def linear_search_blocks(blocks, unique):
    """Reads for a linear search: on a unique key you stop when you find it, half the file on average;
    otherwise you read the whole file. Never less than 1 read."""
    raise NotImplementedError("write this")


def binary_search_blocks(blocks):
    """Reads for a binary search on a file sorted on the key: ceil(log2(blocks)), and at least 1."""
    raise NotImplementedError("write this")


def index_levels(entries, fanout):
    """Levels in a multilevel index whose first level has `entries` entries, `fanout` to a block: each level
    indexes the blocks of the one below, until a level fits in one block."""
    raise NotImplementedError("write this")


def cheapest_lookup(records, record_size, block_size, key_size, pointer_size, sorted_on_key):
    """Kata: find one record by a unique key. Return (method, reads) for the cheapest of
        "linear"           linear_search_blocks on a unique key
        "binary"           only if the file is sorted on the key
        "primary index"    only if sorted: a multilevel index with one entry per data block, then the data block
        "secondary index"  a multilevel index with one entry per record, then the data block
    An index entry is key_size + pointer_size bytes. Ties go to the earlier method in this list."""
    raise NotImplementedError("write this")
