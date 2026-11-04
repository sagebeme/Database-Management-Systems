"""Day 92: sharding, by modulo and by consistent hashing.

Keys and node names are strings. Every hash here is SHA-256, read as a big number, so it's the same on every
machine and every run (Python's own hash() isn't).
"""

import hashlib
from bisect import bisect_right


def h(text):
    """A stable 64-bit hash of a string. (Done for you.)"""
    return int(hashlib.sha256(text.encode()).hexdigest()[:16], 16)


def shard_for(key, shards):
    """The shard (0 to shards - 1) for key, by h(key) modulo the number of shards."""
    return h(key) % shards


def moved_fraction(keys, old_shards, new_shards):
    """The fraction (0 to 1) of keys whose shard_for changes when the number of shards goes from old to new."""
    keys = list(keys)
    moved = sum(1 for k in keys if shard_for(k, old_shards) != shard_for(k, new_shards))
    return moved / len(keys) if keys else 0.0


class Ring:
    """Kata: consistent hashing. Each node owns `replicas` points on a ring of numbers, at h(f"{node}#{i}") for i in
    range(replicas). A key belongs to the first point clockwise from h(key): the smallest point greater than h(key),
    wrapping round to the smallest point of all."""

    def __init__(self, replicas=100):
        self.replicas = replicas
        self.points = []      # sorted point positions
        self.owner = {}       # position -> node

    def add(self, node):
        """Put node's points on the ring."""
        for i in range(self.replicas):
            p = h(f"{node}#{i}")
            self.owner[p] = node
            self.points.insert(bisect_right(self.points, p), p)

    def remove(self, node):
        """Take node's points off the ring."""
        for i in range(self.replicas):
            p = h(f"{node}#{i}")
            if self.owner.get(p) == node:
                del self.owner[p]
                self.points.remove(p)

    def node_for(self, key):
        """The node that owns key. LookupError if the ring is empty."""
        if not self.points:
            raise LookupError("the ring has no nodes")
        i = bisect_right(self.points, h(key))
        return self.owner[self.points[i % len(self.points)]]
