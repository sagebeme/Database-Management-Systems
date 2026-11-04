"""Day 78 capstone: the SACCO's own little storage engine.

A members table kept in a heap file of 4 KB pages, a B+ tree index on id held in memory, and a write-ahead log
so that a power cut never loses a change that was logged.

A row is (id, phone, name, savings): id and savings are integers, phone is 12 characters, name at most 30
bytes of UTF-8.

Files in the table's folder:
    members.heap   the pages
    wal.log        the log: one JSON record per line
"""

import json
import os
import struct
from pathlib import Path

from bplustree import BPlusTree

PAGE_SIZE = 4096
ROW = struct.Struct("<i12s30sq")       # 54 bytes: id, phone, name, savings
HEADER = struct.Struct("<H")           # 2 bytes at the start of each page: how many rows it holds
ROWS_PER_PAGE = (PAGE_SIZE - HEADER.size) // ROW.size
INDEX_ORDER = 64


class Pages:
    """A file of fixed-size pages. Counts every read and write so tests can see what you touch. (Done for you.)"""

    def __init__(self, path):
        self.path = Path(path)
        self.path.touch()
        self.reads = self.writes = 0

    def count(self):
        return self.path.stat().st_size // PAGE_SIZE

    def read_page(self, n):
        if not 0 <= n < self.count():
            raise IndexError(f"there's no page {n}")
        self.reads += 1
        with self.path.open("rb") as f:
            f.seek(n * PAGE_SIZE)
            return bytearray(f.read(PAGE_SIZE))

    def write_page(self, n, data):
        """Write page n (n == count() adds a new page at the end) and make sure it's on disk."""
        if len(data) != PAGE_SIZE:
            raise ValueError(f"a page is {PAGE_SIZE} bytes, not {len(data)}")
        if not 0 <= n <= self.count():
            raise IndexError(f"can't write page {n} of a {self.count()}-page file")
        self.writes += 1
        with self.path.open("r+b") as f:
            f.seek(n * PAGE_SIZE)
            f.write(data)
            f.flush()
            os.fsync(f.fileno())


class Log:
    """An append-only log of JSON records, each forced to disk before append() returns. (Done for you.)"""

    def __init__(self, path):
        self.path = Path(path)
        self.path.touch()

    def append(self, record):
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
            f.flush()
            os.fsync(f.fileno())

    def records(self):
        with self.path.open(encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]


def pack(row):
    """A row as ROW.size bytes. Strings are UTF-8, padded with zero bytes. ValueError if phone isn't exactly 12
    characters or the name is over 30 bytes."""
    raise NotImplementedError("write this")


def unpack(data):
    """The row back from its bytes, without the padding."""
    raise NotImplementedError("write this")


class HeapFile:
    """Rows in pages, in the order they arrive. A row's address (rid) is (page number, slot number)."""

    def __init__(self, pages):
        self.pages = pages

    def insert(self, row):
        """Put the row in the last page if it has room, otherwise in a new page. Return its rid."""
        raise NotImplementedError("write this")

    def get(self, rid):
        """The row at rid, reading exactly one page."""
        raise NotImplementedError("write this")

    def put(self, rid, row):
        """Overwrite the row at rid in place."""
        raise NotImplementedError("write this")

    def scan(self):
        """Every (rid, row), page by page, slot by slot."""
        raise NotImplementedError("write this")


class Table:
    def __init__(self, folder):
        """Open (or create) the table in folder and recover: rebuild the index from the heap with
        BPlusTree.bulk_load, then redo every logged change the heap is missing."""
        raise NotImplementedError("write this")

    def insert(self, row):
        """Add a row: ValueError if the id is taken or the row can't be packed. Log it, then write the page,
        then index it."""
        raise NotImplementedError("write this")

    def get(self, member_id):
        """The row with that id, or None, reading at most one page."""
        raise NotImplementedError("write this")

    def range(self, lo, hi):
        """Rows with lo <= id <= hi, in id order."""
        raise NotImplementedError("write this")

    def update_savings(self, member_id, savings):
        """Kata: set a member's savings. KeyError if there's no such member. Log first, then change the row in
        place; recovery redoes it, and redoing it twice must be harmless."""
        raise NotImplementedError("write this")

    def _set_savings(self, member_id, savings):
        """Change one member's savings in their page. (Part of the kata.)"""
        raise NotImplementedError("write this")
