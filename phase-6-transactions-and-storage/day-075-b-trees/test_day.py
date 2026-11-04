"""Day 75: B-Trees."""

import math
import random

import pytest

from coursekit import load_module


@pytest.fixture
def bt(target):
    return load_module(target / "btree.py")


def build(bt, order, keys):
    t = bt.BTree(order)
    for k in keys:
        t.insert(k)
    return t


def check_shape(tree):
    """Every rule of a B-tree. Returns the keys in order."""
    order, depths, out = tree.order, set(), []

    def walk(node, depth, lo, hi, root):
        assert len(node.keys) <= order - 1, f"a node of order {order} holds {node.keys}"
        if not root:
            assert len(node.keys) >= math.ceil(order / 2) - 1, f"{node.keys} is too empty for order {order}"
        assert node.keys == sorted(node.keys)
        assert all((lo is None or k > lo) and (hi is None or k < hi) for k in node.keys), "keys in the wrong subtree"
        if node.leaf:
            depths.add(depth)
            out.extend(node.keys)
            return
        assert len(node.children) == len(node.keys) + 1
        bounds = [lo] + node.keys + [hi]
        for i, child in enumerate(node.children):
            walk(child, depth + 1, bounds[i], bounds[i + 1], False)
            if i < len(node.keys):
                out.append(node.keys[i])

    walk(tree.root, 1, None, None, True)
    assert len(depths) <= 1, "every leaf must be at the same depth"
    return out


def test_small_trees(bt):
    assert build(bt, 3, []).levels() == [[[]]]
    assert build(bt, 3, [1, 2]).levels() == [[[1, 2]]]
    assert build(bt, 3, [1, 2, 3]).levels() == [[[2]], [[1], [3]]]
    assert build(bt, 3, range(1, 6)).levels() == [[[2, 4]], [[1], [3], [5]]]
    assert build(bt, 3, range(1, 11)).levels() == [[[4]], [[2], [6, 8]], [[1], [3], [5], [7], [9, 10]]]
    assert build(bt, 4, range(10, 100, 10)).levels() == [[[30, 60]], [[10, 20], [40, 50], [70, 80, 90]]]


def test_split_picks_keys_m_over_2(bt):
    assert build(bt, 4, [1, 2, 3, 4]).levels() == [[[3]], [[1, 2], [4]]]
    assert build(bt, 5, [5, 1, 4, 2, 3]).levels() == [[[3]], [[1, 2], [4, 5]]]


def test_duplicates_change_nothing(bt):
    t = build(bt, 3, [5, 3, 8, 5, 3, 3, 8])
    assert t.levels() == [[[5]], [[3], [8]]]


def test_height(bt):
    assert build(bt, 3, []).height() == 1
    assert build(bt, 3, [1, 2]).height() == 1
    assert build(bt, 3, range(1, 11)).height() == 3
    assert build(bt, 200, range(10_000)).height() == 2


def test_search(bt):
    t = build(bt, 3, range(1, 11))
    assert t.search(4) == (True, 1)
    assert t.search(8) == (True, 2)
    assert t.search(10) == (True, 3)
    assert t.search(0) == (False, 3)
    assert t.search(5.5) == (False, 3)
    assert build(bt, 3, []).search(1) == (False, 1)


@pytest.mark.parametrize("order", [3, 4, 5, 7, 16])
def test_random_inserts_keep_every_rule(bt, order):
    rng = random.Random(order)
    keys = [rng.randrange(5000) for _ in range(1500)]
    t = build(bt, order, keys)
    assert check_shape(t) == sorted(set(keys))
    for k in rng.sample(keys, 50):
        found, read = t.search(k)
        assert found and read <= t.height()
    assert t.search(-1) == (False, t.height())


@pytest.mark.parametrize("order", [3, 6])
def test_sorted_inserts_stay_short(bt, order):
    t = build(bt, order, range(2000))
    check_shape(t)
    assert t.height() <= 1 + math.log(2000, math.ceil(order / 2)), "a B-tree stays balanced however you fill it"


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.MOST_KEYS_IN_A_NODE, a.FEWEST_KEYS_IN_A_NODE_THAT_ISNT_THE_ROOT, a.MOST_CHILDREN] == [4, 2, 5]
    assert [a.EVERY_LEAF_IS_AT_THE_SAME_DEPTH, a.A_B_TREE_GROWS_TALLER_AT_THE_LEAVES,
            a.INSERTING_IN_SORTED_ORDER_MAKES_IT_A_LINKED_LIST] == [True, False, False]


def test_kata_between(bt):
    t = build(bt, 3, range(1, 11))
    assert t.between(3, 8) == [3, 4, 5, 6, 7, 8]
    assert t.between(4, 4) == [4]
    assert t.between(4.5, 4.9) == []
    assert t.between(-5, 2) == [1, 2]
    assert t.between(9, 99) == [9, 10]
    assert build(bt, 3, []).between(0, 10) == []
    rng = random.Random(75)
    keys = sorted({rng.randrange(10_000) for _ in range(3000)})
    t = build(bt, 5, rng.sample(keys, len(keys)))
    for lo, hi in [(0, 10_000), (2500, 2600), (9990, 20_000), (100, 99)]:
        assert t.between(lo, hi) == [k for k in keys if lo <= k <= hi]


def test_kata_between_skips_subtrees(bt, monkeypatch):
    t = build(bt, 4, range(10_000))
    opened = set()
    leaf = bt.Node.leaf
    monkeypatch.setattr(bt.Node, "leaf", property(lambda node: opened.add(id(node)) or leaf.fget(node)))
    assert t.between(5000, 5010) == list(range(5000, 5011))
    assert len(opened) < 30, "between() opened nearly the whole tree; skip subtrees that can't hold the range"
