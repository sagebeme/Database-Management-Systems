# Day 78: Capstone: The SACCO Engine

## The brief

Phase 6 has taken the database apart: transactions and their schedules, locks and timestamps, logs and recovery, pages, B-trees and B+ trees, clustered indexes. Today you put the storage half back together and build a working storage engine for a SACCO's members table in about 150 lines of Python.

It keeps rows in **4 KB pages** in a heap file, finds them through a **B+ tree index** (yours, from Day 76), and writes every change to a **write-ahead log** first, so a power cut never loses a change that was logged. The tests cut the power on you.

## What you'll use

**Rows on disk.** A row is `(id, phone, name, savings)`. `struct` turns it into exactly 54 bytes:

```python
ROW = struct.Struct("<i12s30sq")    # int, 12 bytes, 30 bytes, 8-byte int: little-endian, no padding
ROW.pack(7, b"254712345678", b"Wanjiku", 15000)   # strings come out padded with zero bytes
```

Encode strings to UTF-8 *before* checking their length: `"Mūkami"` is 6 characters but 7 bytes.

**A page** (Day 74) is 4,096 bytes: a 2-byte header saying how many rows it holds, then the rows one after another. `(4096 - 2) // 54 = 75` rows to a page. Row `slot` of a page starts at byte `2 + slot * 54`. A row's address, its **rid**, is `(page number, slot)`.

**A heap file** adds rows in arrival order: into the last page if it has room, otherwise a new page. `Pages` (done for you) reads and writes whole pages, and counts them.

**The index** (Days 76 and 77) maps `id` to rid. It lives in memory, so it's rebuilt every time the table opens: scan the heap, sort the `(id, rid)` pairs, and `BPlusTree.bulk_load` them, your Day 76 kata. A lookup is then a walk down the tree in memory and exactly **one page read**.

**The log** (Day 73) is a redo log. `Log` (done for you) appends a JSON record and forces it to disk:

```
{"op": "insert", "row": [7, "254712345678", "Wanjiku", 15000]}
{"op": "update", "id": 7, "savings": 20000}
```

**The rules** that make it crash-safe:

1. **Write-ahead**: log the change before you write the page. If the power goes after the log write, recovery redoes the change. If it goes before, the change never happened, and no page may show it.
2. **Recovery** on open: rebuild the index from the heap, then go through the log in order and redo whatever the heap is missing. An insert whose id is already in the index is already done. An update just sets the value, so doing it twice is harmless (Day 73).

Real engines add much more: LSNs on every page so redo knows what's been applied, undo for uncommitted work, checkpoints so the log doesn't grow forever, a buffer pool so pages aren't read from disk every time. You've met the ideas behind each one this phase.

## Steps

Pure Python. `starter/bplustree.py` is Day 76, finished; `Pages`, `Log` and the constants in `starter/engine.py` are done.

1. `pack` and `unpack`.
2. `HeapFile`: `insert`, `get`, `put`, `scan`. Then reopen the file in a new `HeapFile` and check your rows are still there.
3. `Table`: `__init__` (open and recover), `insert`, `get`, `range`.
4. `pytest phase-6-transactions-and-storage/day-078-capstone-the-sacco-engine`

The tests put 500 members in, in random order, check that a lookup reads one page, reopen the table, and pull the plug part-way through an insert, both just after logging and just before.

## The kata: A Deposit

Write `update_savings(member_id, savings)` and `_set_savings`: log `{"op": "update", ...}`, then change the row in its page with `HeapFile.put`. Recovery must redo logged updates in log order. A test makes the page write fail after the log write and checks the deposit is there when the table reopens.

## When you're stuck

- **`struct.error: argument for 's' must be a bytes object`**: encode strings with `.encode()` before packing.
- **Names come back with `\x00` on the end**: strip the zero bytes (`rstrip(b"\0")`) before decoding.
- **Every row goes into a new page**: read the last page's header (`HEADER.unpack_from(page)`) to see how full it is, and only start page `count()` when it holds 75.
- **"get reads exactly one page"**: don't scan; compute the row's offset in its page from the slot.
- **"reopening must not write the rows again"**: on open, redo an insert only if the index doesn't already have that id.
- **"nothing logged, so nothing may reach the page"**: call `self.log.append` before anything that writes a page, and let its exception stop the insert.
- **"a refused row leaves no trace"**: check the row packs and the id is free *before* logging, or recovery will replay a bad record.
