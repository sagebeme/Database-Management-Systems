# Day 98: Portfolio: Build a Key-Value Store

## The brief

An M-Pesa agent app needs to remember, on each phone, the last name it saw for every number: fast lookups, a few writes a second, and it must survive the battery dying mid-write. A full database is too heavy. You'll build the storage engine yourself, the same design as Bitcask (the engine behind Riak) and the log at the heart of every LSM tree (Day 76's B+ tree has a rival).

The whole idea fits in three sentences:

1. **Never change a byte on disk.** Every write, even a delete, is appended to the end of a log file.
2. **Keep an index in memory**: for each key, which file and where in it its newest value starts. A read is one seek.
3. **Old values pile up.** When a file is full start a new one (a *segment*); now and then **compact**: copy the live values into fresh segments and delete the old ones.

No walkthrough: the contract is below, and the tests are the acceptance checks.

## What you'll use

**The record format** is done for you in `encode` and `read_records`:

```
| crc32 (4) | key length (4) | value length (4, -1 = deleted) | key bytes | value bytes |
```

The checksum covers everything after it, so a record cut short by a crash, or a flipped bit, is caught.

**What you write in `starter/kv.py`**:

| Method | Does |
|---|---|
| `_load()` | Called when the store opens. Read every segment oldest first to rebuild `self.index` (`key -> Where(segment, offset, size)`, with `offset` where the *value* starts). A later record wins; a tombstone removes the key. A bad record at the end of the **newest** segment is a crash mid-write: cut the file off there (`truncate`). A bad record anywhere else is real damage: raise `CorruptError`. Then open the newest segment (or `000001.log`) for appending as `self.file`, its number in `self.active`. |
| `_append(key, value)` | Append one record, starting a new segment first if the active one has reached `max_segment_bytes`. Flush it. Return its offset. |
| `put(key, value)` | Values are `bytes` (`TypeError` otherwise). |
| `get(key)` | Bytes, or `None`. Read from disk: the index holds positions, not values. |
| `delete(key)` | Append a tombstone. `True` if the key existed. |
| `keys()` | Live keys, sorted. |
| `compact()` | Write every live value into new segments numbered after all existing ones (`fsync` them), *then* delete the old segments. The last new segment becomes the active one. |

Segment files are `000001.log`, `000002.log`, and so on, with higher numbers newer.

**Why the order matters in `compact`**: if the power goes off after the new segments are written but before every old one is deleted, the next `_load` reads the old ones first and the new ones last, so the newer copies win and nothing is lost. Delete first and a crash loses data. The test pulls the plug halfway through to check.

**Why tombstones vanish safely in compaction**: a deleted key has no live value, so nothing is copied for it, and the old segments holding its earlier values are deleted in the same compaction. If you kept even one old segment, the key would come back from the dead.

## Steps

1. Fill in the methods in `starter/kv.py`.
2. `pytest phase-8-expert/day-098-portfolio-build-a-key-value-store`
3. Try it by hand:

   ```python
   from kv import KV
   s = KV("/tmp/agent")
   s.put("254712345678", b"Wanjiku")
   s.close()
   KV("/tmp/agent").get("254712345678")
   ```

4. For your portfolio, measure it: time 100,000 puts and gets, and show the disk size before and after compaction in the README.

## The kata: When to Compact

Compacting too often wastes writes; too rarely wastes disk. Write `dead_ratio()`: the share of bytes on disk that no reader can see (overwritten values, tombstones, their headers), `0.0` for an empty store. And `maybe_compact(threshold=0.5)`: compact only when more than `threshold` of the bytes are dead, and return whether it did.

## When you're stuck

- **`get` returns the key glued to the value**: the index offset should point at the value, after the 12-byte header and the key's *encoded* length (`len(key.encode())`, not `len(key)`: `✓` is three bytes).
- **The torn-write test says the file wasn't cut**: open the segment with `"r+b"` and `truncate(offset)` at the bad record.
- **The corruption test doesn't raise**: only the newest segment may have a torn tail. In an older one, a bad record means damage.
- **A deleted key comes back after a restart**: `_load` must apply tombstones in order, removing the key from the index.
- **A deleted key comes back after compaction**: an old segment survived compaction. Delete all the segments that existed before it started.
- **Values from before the restart win over newer ones**: read segments in number order, and within a file in offset order.
- **`dead_ratio` is off by a little**: count the whole record (header and key too) as live for every key in the index, and everything else on disk as dead.
