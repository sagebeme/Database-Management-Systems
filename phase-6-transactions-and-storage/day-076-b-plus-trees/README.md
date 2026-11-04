# Day 76: B+ Trees

## The brief

Day 75's kata showed the B-tree's weak spot: "every member who joined in March" means keys scattered over leaves *and* inner nodes, and climbing up and down the tree to collect them. Real databases use a small change, the **B+ tree**, and it's the structure behind nearly every index you'll ever create: InnoDB tables and indexes, Postgres's default index, SQLite and many file systems.

Two changes make the difference. All the data lives in the leaves, and the leaves are linked in a chain. Today you'll build one, and then build one the fast way, bottom-up from sorted data, the way `CREATE INDEX` does.

## What you'll use

A B+ tree of order `m` holds at most `m - 1` keys in a node, like a B-tree. The differences:

- **Every key, with its value (the row, or a pointer to it), is in a leaf.** Inner nodes hold only *copies* of keys to steer the search, so they're small, more of them fit in a page, and the fan-out is bigger.
- **Leaves are linked left to right.** A range scan finds the first leaf and walks along the bottom.
- **The separator rule**: child `i` holds keys `k` with `keys[i-1] <= k < keys[i]`. A key equal to a separator is on the *right*, so search with `bisect_right`.

**Splitting** is slightly different at the two levels:

| | stays left | goes right | goes up |
|---|---|---|---|
| Leaf with `m` keys | `keys[:m//2]` | `keys[m//2:]` | a **copy** of the right leaf's first key |
| Inner node with `m` keys | `keys[:m//2]` | `keys[m//2+1:]` | `keys[m//2]` itself (it **moves**) |

The leaf split copies, because every key must stay in a leaf. The inner split moves, as in a B-tree, because inner keys are only signposts.

Order 3, inserting 1, 2, 3:

```
[1 2]  insert 3 -> [1 2 3] is full:      [2]
                                     [1] -> [2 3]
```

**Bulk loading**: inserting a million sorted keys one at a time splits nodes over and over and leaves every leaf half full. When the data is already sorted, fill the leaves left to right, then build each level above from the one below. Databases do this when you `CREATE INDEX` on an existing table, or `ALTER TABLE ... ADD INDEX` (InnoDB calls it a *sorted index build*).

## Steps

1. `starter/bplustree.py`: `Node`, the constructor and `_leaf_for` are done. Write `get`, `insert` (with `_insert`), `leaves`, `levels` and `range`.
2. Draw order 3 with 1 to 7 inserted, and order 4 with 10, 20, ..., 90, before you code. The tests check those shapes.
3. `starter/answers.py`.
4. `pytest phase-6-transactions-and-storage/day-076-b-plus-trees`

## The kata: Build It from the Bottom

In `starter/bplustree.py`, write the class method `bulk_load(order, pairs)`. Pack the leaves full, link them, and build the levels above. Watch the last node of each level: it may be too empty to be legal, and then the last two nodes share what they have. Tests check exact shapes, every B+ tree rule for orders 3 to 50 and up to 5,000 keys, and that the tree still takes inserts afterwards.

## When you're stuck

- **`get` misses keys that are separators**: equal keys are to the *right*. `_leaf_for` uses `bisect_right`; inside a leaf, use `bisect_left` to find the exact position.
- **A leaf split loses the separator from the leaves**: a leaf split *copies* the first key of the right leaf up; it stays in the leaf too.
- **"each leaf's `next` must be the leaf to its right"**: the new right leaf's `next` is the old leaf's `next`, and the old leaf's `next` becomes the new leaf. In that order.
- **"keys in the wrong subtree" after an inner split**: the middle key moves up and is in *neither* half.
- **`range` misses the first key**: start from `_leaf_for(lo)` and skip keys below `lo` in that leaf only.
- **Bulk load: "leaf is too empty"**: the minimum is `ceil((order - 1) / 2)` keys for a leaf and `ceil(order / 2)` children for an inner node. When the last group is short, join it with the one before and split the total in two, the left one getting the extra.
- **Bulk load: the separators are wrong at level 2**: an inner node's key for a child is the smallest key *anywhere under* that child: go down its leftmost path to a leaf.
