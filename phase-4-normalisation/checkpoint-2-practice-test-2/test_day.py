"""Checkpoint 2: Practice Test 2. Each question is one test; your score is the marks of the ones that pass.

The answers are stored as SHA-256 hashes, so reading this file won't give them away.
"""

import hashlib

import pytest

from coursekit import load_module

ANSWER_HASHES = {
    1: "c21f5cf9073ee25fb3b274a34af9288fb8795e5ff3404002f1867154c0b3f762",
    2: "f4e933abf7446a9651711b2ebedc48f126d4f11e3ed08e92bfc958953b099b64",
    3: "7bc5b302350f71e7a0fe1c8a74b334389fb203662ec8a50f026e2ed630423c09",
    4: "3727dc1d8803d5e5a4300374e11a30363158f2abd9a3cea01d53d12102ecb0df",
    5: "3ddbbc330681f5a53363261a876100a6459dd596d064b3926ab32a849078226a",
    6: "24557ad813faaa5a09cf3fd8f59ccb8b13a979bbddbf3261cfb36b6204305cab",
    7: "122b6ebda4dbd935400d72d70c621531a6b6037c164110ee5aa87b3bd4fe91b2",
    8: "fffa8d07eb037e75c4c37d2d68a37177f8eea04400ac9a16fa674ce233e1844c",
    9: "5ebb2cd4fc85f9f8cfb082641a1430330bead229ed3b3148dd23e7d6d82920bb",
    10: "fe25bd615e0275e280ce4e7acd66df613e198b0aefd7a4964e3cd5cd48f4593c",
    11: "c460c209422e88c643e4c42dfa46143b3affa01f296db76288cc8a739db6a7c9",
    12: "9c8e1d49f07ea8a8147f057abae9ef1b38fa2e3c8436296cf52bbe574d673be3",
    13: "a206e74b8103f26a60bcac5c6dc137de7e64dd81506062229dde132d03a3def3",
    14: "49dce45f55fd3a7324e8b623d680af1e6137e75e5e73919a605f23661896da76",
    15: "55be7cb18d38ec2a70e6d410745be90cd3e9fc3d8ee64b6733d60ff465cd5959",
    16: "2183a3543acad5d35e56e820a0555ad7a983ced8e3e4f98a93ef60b539c332f0",
}
MARKS = {1: 1, 2: 2, 3: 1, 4: 2, 5: 2, 6: 2, 7: 1, 8: 2, 9: 1, 10: 1, 11: 2, 12: 2, 13: 2, 14: 2, 15: 1, 16: 2}


def normalise(value):
    if isinstance(value, bool) or value is None:
        return repr(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, (set, frozenset, list, tuple)):
        return ",".join(sorted(str(x).strip().upper() for x in value))
    return str(value).strip().upper()


@pytest.fixture
def answers(target):
    return load_module(target / "answers.py")


@pytest.mark.parametrize("question", sorted(ANSWER_HASHES))
def test_question(answers, question):
    given = getattr(answers, f"Q{question}")
    assert given is not None, f"Q{question} is still None"
    digest = hashlib.sha256(f"cp2:{question}:{normalise(given)}".encode()).hexdigest()
    assert digest == ANSWER_HASHES[question], f"Q{question} ({MARKS[question]} marks): not this one"
