"""Day 76: a B+ tree, the index every relational database uses.

Order m, as on Day 75: at most m - 1 keys in any node. The differences:
- Every key and its value live in a leaf. Inner nodes hold only copies of keys, to steer searches.
- Leaves are linked left to right through `next`, so a range scan walks along the bottom.
- Child i of an inner node holds keys k with keys[i - 1] <= k < keys[i]: search with bisect_right.

Leaf split (a leaf reaches m keys): the left leaf keeps keys[:m // 2], a new right leaf gets keys[m // 2:], and
a *copy* of the right leaf's first key goes up into the parent. Fix the `next` links.
Inner split (an inner node reaches m keys): as in a B-tree, keys[m // 2] *moves* up; the left keeps
keys[:m // 2], the right gets keys[m // 2 + 1:], the children are split to match.
A key that's already there gets its value replaced.
"""

from bisect import bisect_left, bisect_right
from dataclasses import dataclass, field


@dataclass(eq=False)
class Node:
    keys: list = field(default_factory=list)
    children: list = field(default_factory=list)   # inner nodes only
    values: list = field(default_factory=list)     # leaves only, one per key
    next: "Node | None" = None                     # leaves only: the leaf to the right

    @property
    def leaf(self):
        return not self.children


class BPlusTree:
    def __init__(self, order):
        if order < 3:
            raise ValueError("a B+ tree needs order 3 or more")
        self.order = order
        self.root = Node()

    def _leaf_for(self, key):
        """The leaf where key is, or would be."""
        node = self.root
        while not node.leaf:
            node = node.children[bisect_right(node.keys, key)]
        return node

    def get(self, key):
        """The value stored under key, or None."""
        raise NotImplementedError("write this")

    def insert(self, key, value):
        """Store value under key, splitting on the way back up as needed."""
        raise NotImplementedError("write this")

    def _insert(self, node, key, value):
        """Insert into the subtree under node. Return None, or (separator, new_right_node) if node split."""
        raise NotImplementedError("write this")

    def leaves(self):
        """The keys of every leaf, left to right, found by following `next` from the leftmost leaf."""
        raise NotImplementedError("write this")

    def levels(self):
        """The keys of every node, level by level from the root, left to right (as on Day 75)."""
        raise NotImplementedError("write this")

    def range(self, lo, hi):
        """Every (key, value) with lo <= key <= hi, in key order: find lo's leaf, then walk along `next`."""
        raise NotImplementedError("write this")

    @classmethod
    def bulk_load(cls, order, pairs):
        """Kata: build a tree bottom-up from (key, value) pairs sorted by key, with no duplicate keys.
        Fill each leaf with order - 1 keys, left to right. If the last leaf ends up with fewer than
        ceil((order - 1) / 2) keys, share the last two leaves' keys between them, the left one getting the extra
        key if the total is odd. Then build each level above the same way: up to `order` children per node, the
        last two shared out if the last node would have fewer than ceil(order / 2) children. An inner node's
        keys are the smallest key under each of its children but the first."""
        raise NotImplementedError("write this")
