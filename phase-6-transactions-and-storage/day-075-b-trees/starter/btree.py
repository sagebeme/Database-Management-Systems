"""Day 75: a B-tree.

A B-tree of order m: every node holds at most m - 1 keys and m children; every node except the root holds at
least ceil(m / 2) - 1 keys; every leaf is at the same depth. Keys are unique; inserting one that's already
there changes nothing.

Splitting: when an insert leaves a node with m keys, take its middle key keys[m // 2] up into the parent; the
keys to its left stay in this node and the keys to its right go to a new node, with the children split the
same way. A root that splits makes a new root with that one key.
"""

from bisect import bisect_left
from dataclasses import dataclass, field


@dataclass
class Node:
    keys: list = field(default_factory=list)
    children: list = field(default_factory=list)   # empty for a leaf; otherwise len(keys) + 1 nodes

    @property
    def leaf(self):
        return not self.children


class BTree:
    def __init__(self, order):
        if order < 3:
            raise ValueError("a B-tree needs order 3 or more")
        self.order = order
        self.root = Node()

    def search(self, key):
        """(found, nodes_read): whether the key is in the tree, and how many nodes you looked at to find out."""
        raise NotImplementedError("write this")

    def insert(self, key):
        """Add the key, splitting nodes on the way back up as needed."""
        raise NotImplementedError("write this")

    def _insert(self, node, key):
        """Insert into the subtree under node. Return None, or (middle_key, new_right_node) if node split."""
        raise NotImplementedError("write this")

    def height(self):
        """Levels in the tree: 1 for a lone root (even an empty one)."""
        raise NotImplementedError("write this")

    def levels(self):
        """The keys of every node, level by level from the root, left to right: a list of lists of lists.
        BTree(3) after inserting 1 to 5: [[[2, 4]], [[1], [3], [5]]]"""
        raise NotImplementedError("write this")

    def between(self, lo, hi):
        """Kata: every key k with lo <= k <= hi, in order. Only go into subtrees that can hold such keys."""
        raise NotImplementedError("write this")
