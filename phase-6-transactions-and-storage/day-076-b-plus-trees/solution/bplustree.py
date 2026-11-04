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
        leaf = self._leaf_for(key)
        i = bisect_left(leaf.keys, key)
        return leaf.values[i] if i < len(leaf.keys) and leaf.keys[i] == key else None

    def insert(self, key, value):
        """Store value under key, splitting on the way back up as needed."""
        split = self._insert(self.root, key, value)
        if split:
            separator, right = split
            self.root = Node([separator], [self.root, right])

    def _insert(self, node, key, value):
        """Insert into the subtree under node. Return None, or (separator, new_right_node) if node split."""
        m = self.order
        if node.leaf:
            i = bisect_left(node.keys, key)
            if i < len(node.keys) and node.keys[i] == key:
                node.values[i] = value
                return None
            node.keys.insert(i, key)
            node.values.insert(i, value)
            if len(node.keys) < m:
                return None
            mid = m // 2
            right = Node(node.keys[mid:], values=node.values[mid:], next=node.next)
            node.keys, node.values, node.next = node.keys[:mid], node.values[:mid], right
            return right.keys[0], right
        i = bisect_right(node.keys, key)
        split = self._insert(node.children[i], key, value)
        if split is None:
            return None
        separator, new = split
        node.keys.insert(i, separator)
        node.children.insert(i + 1, new)
        if len(node.keys) < m:
            return None
        mid = m // 2
        up = node.keys[mid]
        right = Node(node.keys[mid + 1:], node.children[mid + 1:])
        node.keys, node.children = node.keys[:mid], node.children[:mid + 1]
        return up, right

    def leaves(self):
        """The keys of every leaf, left to right, found by following `next` from the leftmost leaf."""
        node = self.root
        while not node.leaf:
            node = node.children[0]
        out = []
        while node:
            out.append(node.keys[:])
            node = node.next
        return out

    def levels(self):
        """The keys of every node, level by level from the root, left to right (as on Day 75)."""
        out, level = [], [self.root]
        while level:
            out.append([n.keys[:] for n in level])
            level = [c for n in level for c in n.children]
        return out

    def range(self, lo, hi):
        """Every (key, value) with lo <= key <= hi, in key order: find lo's leaf, then walk along `next`."""
        leaf, out = self._leaf_for(lo), []
        while leaf:
            for k, v in zip(leaf.keys, leaf.values):
                if k > hi:
                    return out
                if k >= lo:
                    out.append((k, v))
            leaf = leaf.next
        return out

    @classmethod
    def bulk_load(cls, order, pairs):
        """Kata: build a tree bottom-up from (key, value) pairs sorted by key, with no duplicate keys.
        Fill each leaf with order - 1 keys, left to right. If the last leaf ends up with fewer than
        ceil((order - 1) / 2) keys, share the last two leaves' keys between them, the left one getting the extra
        key if the total is odd. Then build each level above the same way: up to `order` children per node, the
        last two shared out if the last node would have fewer than ceil(order / 2) children. An inner node's
        keys are the smallest key under each of its children but the first."""
        tree = cls(order)
        pairs = list(pairs)
        if not pairs:
            return tree

        def chunks(items, size, least):
            groups = [items[i:i + size] for i in range(0, len(items), size)]
            if len(groups) > 1 and len(groups[-1]) < least:
                both = groups[-2] + groups[-1]
                half = (len(both) + 1) // 2
                groups[-2:] = [both[:half], both[half:]]
            return groups

        def smallest(node):
            while not node.leaf:
                node = node.children[0]
            return node.keys[0]

        level = [Node([k for k, _ in g], values=[v for _, v in g])
                 for g in chunks(pairs, order - 1, -(-(order - 1) // 2))]
        for a, b in zip(level, level[1:]):
            a.next = b
        while len(level) > 1:
            level = [Node([smallest(c) for c in g[1:]], g) for g in chunks(level, order, -(-order // 2))]
        tree.root = level[0]
        return tree
