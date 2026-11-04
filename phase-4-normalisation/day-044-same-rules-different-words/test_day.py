"""Day 44: Same Rules, Different Words."""

import pytest

from coursekit import load_module
from coursekit.fds import attrs, parse


def fd(text):
    return parse(text)[0]


@pytest.fixture
def ax(target):
    return load_module(target / "axioms.py")


def test_the_three_axioms(ax):
    assert ax.reflexivity(attrs("AB"), attrs("A")) == fd("AB->A")
    with pytest.raises(ValueError):
        ax.reflexivity(attrs("A"), attrs("B"))
    assert ax.augmentation(fd("A->B"), attrs("C")) == fd("AC->BC")
    assert ax.transitivity(fd("A->B"), fd("B->C")) == fd("A->C")
    with pytest.raises(ValueError):
        ax.transitivity(fd("A->B"), fd("C->D"))


def test_the_derived_rules(ax):
    assert ax.union(fd("A->B"), fd("A->C")) == fd("A->BC")
    with pytest.raises(ValueError):
        ax.union(fd("A->B"), fd("C->D"))
    assert ax.decomposition(fd("A->BC"), attrs("B")) == fd("A->B")
    with pytest.raises(ValueError):
        ax.decomposition(fd("A->BC"), attrs("D"))
    assert ax.pseudotransitivity(fd("A->B"), fd("CB->D")) == fd("AC->D")
    with pytest.raises(ValueError):
        ax.pseudotransitivity(fd("A->B"), fd("C->D"))


def test_implies(ax):
    f = parse("A->B; B->C; CD->E")
    assert ax.implies(f, fd("A->C"))
    assert ax.implies(f, fd("AD->E"))
    assert ax.implies(f, fd("AB->A")), "trivial FDs always follow"
    assert not ax.implies(f, fd("C->A"))
    assert not ax.implies(f, fd("A->E"))


@pytest.mark.parametrize("f, g, same", [
    ("A->C; AC->D; E->AD; E->H", "A->CD; E->AH", True),
    ("A->B; B->C", "A->B; A->C", False),
    ("A->B; B->C; A->C", "A->B; B->C", True),
    ("AB->C", "A->C", False),
    ("A->BC", "A->B; A->C", True),
])
def test_equivalent(ax, f, g, same):
    assert ax.equivalent(parse(f), parse(g)) is same


def test_answers(target):
    a = load_module(target / "answers.py")
    assert [a.AB_TO_A, a.A_TO_B_GIVES_AC_TO_BC, a.A_TO_B_AND_B_TO_C_GIVES_A_TO_C, a.A_TO_B_AND_A_TO_C_GIVES_A_TO_BC,
            a.A_TO_BC_GIVES_A_TO_B, a.A_TO_B_AND_CB_TO_D_GIVES_AC_TO_D] == [
        "reflexivity", "augmentation", "transitivity", "union", "decomposition", "pseudotransitivity"]
    assert [a.THE_AXIOMS_ARE_SOUND, a.THE_AXIOMS_ARE_COMPLETE, a.UNION_IS_ONE_OF_THE_THREE_AXIOMS,
            a.AB_TO_C_GIVES_A_TO_C] == [True, True, False, False]


def test_kata_spot_the_spare(ax):
    f = parse("A->B; B->C; A->C; C->D")
    assert ax.redundant(f) == [fd("A->C")]
    g = parse("A->B; B->A; A->C; B->C")
    assert ax.redundant(g) == [fd("A->C"), fd("B->C")], "each is spare on its own, though not both at once"
    assert ax.redundant(parse("A->B; C->D")) == []
