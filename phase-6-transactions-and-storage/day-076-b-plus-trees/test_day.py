"""Day 76: B+ Trees."""

import math
import random

import pytest

from coursekit import load_module


@pytest.fixture
def bp(target):
    return load_module(target / "bplustree.py")


def build(bp, order, keys):
    t = bp.BPlusTree(order)
    for k in keys:
        t.insert(k, f"v{k}")
    return t


def check_shape(tree):
    """Every rule of a B+ tree. Returns the leaves in order, found by walking down (not by `next`)."""
    m, depths, leaves = tree.order, set(), []

    def walk(node, depth, lo, hi, root):
        assert len(node.keys) <= m - 1, f"{node.keys} is too full for order {m}"
        assert node.keys == sorted(set(node.keys))
        assert all((lo is None or k >= lo) and (hi is None or k < hi) for k in node.keys), "keys in the wrong subtree"
        if node.leaf:
            assert len(node.values) == len(node.keys)
            if not root:
                assert len(node.keys) >= math.ceil((m - 1) / 2), f"leaf {node.keys} is too empty for order {m}"
            depths.add(depth)
            leaves.append(node)
            return
        assert len(node.children) == len(node.keys) + 1
        if not root:
            assert len(node.children) >= math.ceil(m / 2), f"inner node {node.keys} has too few children"
        bounds = [lo] + node.keys + [hi]
        for i, child in enumerate(node.children):
            walk(child, depth + 1, bounds[i], bounds[i + 1], False)

    walk(tree.root, 1, None, None, True)
    assert len(depths) == 1, "every leaf must be at the same depth"
    for a, b in zip(leaves, leaves[1:]):
        assert a.next is b, "each leaf's `next` must be the leaf to its right"
    assert leaves[-1].next is None
    return [leaf.keys for leaf in leaves]


def test_small_trees(bp):
    assert build(bp, 3, []).levels() == [[[]]]
    assert build(bp, 3, [1, 2]).levels() == [[[1, 2]]]
    assert build(bp, 3, [1, 2, 3]).levels() == [[[2]], [[1], [2, 3]]], "a leaf split copies 2 up; 2 stays in a leaf"
    assert build(bp, 3, range(1, 8)).levels() == [[[3, 5]], [[2], [4], [6]], [[1], [2], [3], [4], [5], [6, 7]]]
    assert build(bp, 4, range(10, 100, 10)).levels() == [[[30, 50, 70]], [[10, 20], [30, 40], [50, 60], [70, 80, 90]]]


def test_leaves_follow_next(bp):
    t = build(bp, 3, range(1, 8))
    assert t.leaves() == [[1], [2], [3], [4], [5], [6, 7]]
    first = t.root
    while first.children:
        first = first.children[0]
    first.next = first.next.next.next
    assert t.leaves() == [[1], [4], [5], [6, 7]], "leaves() must walk the `next` links"


def test_get_and_replace(bp):
    t = build(bp, 3, [5, 1, 9, 3, 7])
    assert [t.get(k) for k in (1, 3, 5, 7, 9)] == ["v1", "v3", "v5", "v7", "v9"]
    assert t.get(4) is None and t.get(100) is None
    t.insert(5, "five")
    assert t.get(5) == "five"
    assert sum(t.leaves(), []) == [1, 3, 5, 7, 9]
    assert build(bp, 3, []).get(1) is None


@pytest.mark.parametrize("order", [3, 4, 5, 8, 33])
def test_random_inserts_keep_every_rule(bp, order):
    rng = random.Random(order)
    t, want = bp.BPlusTree(order), {}
    for _ in range(2000):
        k = rng.randrange(3000)
        t.insert(k, k * 2)
        want[k] = k * 2
    assert check_shape(t) == t.leaves()
    assert sum(t.leaves(), []) == sorted(want)
    assert all(t.get(k) == v for k, v in want.items())
    assert t.get(-1) is None


def test_range(bp):
    t = build(bp, 3, range(0, 100, 5))
    assert t.range(12, 31) == [(15, "v15"), (20, "v20"), (25, "v25"), (30, "v30")]
    assert t.range(15, 15) == [(15, "v15")]
    assert t.range(-50, 6) == [(0, "v0"), (5, "v5")]
    assert t.range(93, 500) == [(95, "v95")]
    assert t.range(41, 44) == []
    assert t.range(60, 50) == []
    rng = random.Random(76)
    keys = rng.sample(range(10_000), 2500)
    t = build(bp, 6, keys)
    for lo, hi in [(0, 10_000), (4000, 4100), (9999, 9999)]:
        assert [k for k, _ in t.range(lo, hi)] == sorted(k for k in keys if lo <= k <= hi)


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.EVERY_KEY_IS_IN_A_LEAF, a.A_KEY_IN_AN_INNER_NODE_IS_ALWAYS_ALSO_IN_A_LEAF,
            a.A_RANGE_SCAN_NEEDS_TO_CLIMB_BACK_UP_THE_TREE,
            a.INNER_NODES_HOLD_MORE_KEYS_PER_PAGE_THAN_A_B_TREE_NODE_WITH_ROWS_IN_IT,
            a.A_LEAF_SPLIT_MOVES_THE_SEPARATOR_UP] == [True, False, False, True, False]


@pytest.mark.parametrize("order, n, levels", [
    (4, 10, [[[4, 7, 9]], [[1, 2, 3], [4, 5, 6], [7, 8], [9, 10]]]),
    (4, 7, [[[4, 6]], [[1, 2, 3], [4, 5], [6, 7]]]),
    (3, 9, [[[7]], [[3, 5], [9]], [[1, 2], [3, 4], [5, 6], [7, 8], [9]]]),
    (5, 4, [[[1, 2, 3, 4]]]),
    (5, 0, [[[]]]),
])
def test_kata_bulk_load_shapes(bp, order, n, levels):
    t = bp.BPlusTree.bulk_load(order, [(k, f"v{k}") for k in range(1, n + 1)])
    assert t.levels() == levels


@pytest.mark.parametrize("order", [3, 4, 5, 7, 50])
@pytest.mark.parametrize("n", [1, 2, 3, 10, 100, 999, 5000])
def test_kata_bulk_load_rules(bp, order, n):
    pairs = [(k * 3, k) for k in range(n)]
    t = bp.BPlusTree.bulk_load(order, pairs)
    check_shape(t)
    assert len(t.leaves()) == math.ceil(n / (order - 1)), "pack the leaves full"
    assert [t.get(k) for k, _ in pairs[::97]] == [v for _, v in pairs[::97]]
    t.insert(-1, "new")
    check_shape(t)
    assert t.get(-1) == "new", "a bulk-loaded tree takes inserts like any other"
