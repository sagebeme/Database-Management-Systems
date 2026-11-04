# Day 75: B-Trees

## The brief

Day 74 ended with a multilevel index: an index on the index, until the top fits in one page. That works for a file that never changes. The SACCO's members table changes all day: new members join in the middle of the alphabet, and a static index would need rebuilding every time.

The **B-tree** (Bayer and McCreight, 1970) is a multilevel index that stays balanced as you insert. Every node is a disk page holding many keys, every leaf is at the same depth, and the tree grows by splitting full nodes, upwards, so it only ever gets taller at the root. Today you'll build one in Python.

## What you'll use

A B-tree of **order m**:

- every node holds at most `m - 1` keys, sorted, and (if it isn't a leaf) one more child than keys;
- every node except the root holds at least `ceil(m/2) - 1` keys, so it's at least about half full;
- every leaf is at the same depth.

The keys in a node split the key space: everything in `children[i]` is between `keys[i-1]` and `keys[i]`.

**Search**: in each node, find where the key would go (`bisect_left`); either it's there, or go down into that child. One node read per level.

**Insert**: go down to the leaf where the key belongs and put it there. If the leaf now has `m` keys, **split** it: the middle key `keys[m // 2]` moves up into the parent, the keys to its left stay, the keys to its right go into a new node. The parent may now be full, so it splits too, and so on. When the root splits, a new root is made with one key: that's the only way the tree gets taller.

Order 3, inserting 1 to 5:

```
[1 2]        insert 3 -> [1 2 3] is full, 2 goes up:      [2]
                                                         [1] [3]
insert 4, 5 -> [3 4 5] is full, 4 goes up:               [2 4]
                                                      [1] [3] [5]
```

**Why it matters**: with pages of 16 KB and keys plus pointers of about 20 bytes, real B-trees have orders in the hundreds. Three levels hold millions of keys, and the top level or two are always in memory, so finding any row costs one or two disk reads.

**Deleting** (not today) is the mirror image: a node that drops below half full borrows a key from a sibling or merges with it.

## Steps

1. `starter/btree.py`: `Node` and the constructor are done. Write `search`, `insert` (with the helper `_insert`), `height` and `levels`.
2. Draw a few trees on paper first: order 3, insert 1 to 10; order 4, insert 10, 20, ..., 90. The tests check those exact shapes.
3. `starter/answers.py`.
4. `pytest phase-6-transactions-and-storage/day-075-b-trees`

The tests also insert 1,500 random keys into trees of orders 3 to 16 and check every rule, so a split that's nearly right will be caught.

## The kata: Everything in Between

In `starter/btree.py`, write `between(lo, hi)`: every key from `lo` to `hi`, in order. Walk the tree in order (child 0, key 0, child 1, key 1, ..., last child), but skip a subtree when no key in it can be in range. A test counts the nodes you open.

Notice how awkward this is: the keys in range are spread over leaves *and* inner nodes, so you keep climbing up and down. Day 76's B+ tree fixes that.

## When you're stuck

- **`ValueError: a B-tree needs order 3 or more`**: done for you; orders below 3 can't split into two legal halves.
- **The shape is right for order 3 but wrong for order 4**: the middle key is `keys[m // 2]` *after* the insert, when the node holds `m` keys. Left gets `keys[:m // 2]`, right gets `keys[m // 2 + 1:]`.
- **Children go missing after a split**: a node with `k` keys has `k + 1` children. Left keeps `children[:m // 2 + 1]`, right gets the rest.
- **The root split loses the tree**: when `_insert` on the root returns a split, make a new root holding the middle key with the old root and the new node as children.
- **"every leaf must be at the same depth"**: never add a level anywhere except at the root.
- **`search` returns the wrong count**: count every node you look at, including the one where you find the key.
