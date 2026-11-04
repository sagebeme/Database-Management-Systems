"""Day 43: Closure."""

import pytest

from coursekit import load_module
from coursekit.fds import attrs, parse

EXAMPLES = [  # (schema, FDs, candidate keys)
    ("ABCDE", "A->B; BC->E; ED->A", ["ACD", "BCD", "CDE"]),
    ("ABCDEF", "AB->C; C->D; D->E; E->F", ["AB"]),
    ("ABCD", "A->B; B->C; C->D; D->A", ["A", "B", "C", "D"]),
    ("WXYZ", "Z->W; Y->XZ; WX->Y", ["Y", "WX", "XZ"]),
    ("ABCD", "AB->C; C->D; D->A", ["AB", "BC", "BD"]),
    ("ABC", "", ["ABC"]),
]


@pytest.fixture
def cl(target):
    return load_module(target / "closure.py")


def test_closure(cl):
    fds = parse("A->B; BC->E; ED->A")
    assert cl.closure(attrs("A"), fds) == attrs("AB")
    assert cl.closure(attrs("AC"), fds) == attrs("ABCE")
    assert cl.closure(attrs("CD"), fds) == attrs("CD")
    assert cl.closure(attrs("CDE"), fds) == attrs("ABCDE")
    assert cl.closure(attrs("adm_no"), parse("adm_no -> name; name -> house")) == attrs("adm_no name house")


def test_superkey_and_candidate_key(cl):
    fds = parse("A->B; BC->E; ED->A")
    assert cl.is_superkey(attrs("ACD"), attrs("ABCDE"), fds)
    assert cl.is_superkey(attrs("ABCD"), attrs("ABCDE"), fds)
    assert not cl.is_superkey(attrs("AC"), attrs("ABCDE"), fds)
    assert cl.is_candidate_key(attrs("ACD"), attrs("ABCDE"), fds)
    assert not cl.is_candidate_key(attrs("ABCD"), attrs("ABCDE"), fds), "ACD inside it is already a key"


@pytest.mark.parametrize("schema, fds, keys", EXAMPLES)
def test_candidate_keys(cl, schema, fds, keys):
    assert cl.candidate_keys(attrs(schema), parse(fds)) == [attrs(k) for k in keys]


def test_prime_attributes(cl):
    assert cl.prime_attributes(attrs("ABCDE"), parse("A->B; BC->E; ED->A")) == attrs("ABCDE")
    assert cl.prime_attributes(attrs("ABCDEF"), parse("AB->C; C->D; D->E; E->F")) == attrs("AB")


def test_a_bigger_one_is_fast(cl):
    schema = attrs("ABCDEFGHIJKLMN")
    fds = parse("A->B; B->C; C->D; D->E; E->F; F->G; G->H; H->I; I->J; J->K; K->L; L->M; M->N; N->A")
    assert len(cl.candidate_keys(schema, fds)) == 14


def test_answers(target):
    a = load_module(target / "answers.py")
    assert (a.CLOSURE_OF_C, a.CLOSURE_OF_AB) == ("ACD", "ABCD")
    assert (a.NUMBER_OF_CANDIDATE_KEYS, a.NUMBER_OF_PRIME_ATTRIBUTES, a.NUMBER_OF_SUPERKEYS) == (3, 4, 7)
    assert a.ATTRIBUTE_IN_EVERY_KEY == "B"


@pytest.mark.parametrize("schema, fds, expected", [
    ("ABCD", "AB->C; C->D; D->A", 7),
    ("ABCDE", "A->B; BC->E; ED->A", 7),
    ("ABCD", "A->B; B->C; C->D; D->A", 15),
    ("ABC", "", 1),
])
def test_kata_count_them(cl, schema, fds, expected):
    assert cl.count_superkeys(attrs(schema), parse(fds)) == expected
