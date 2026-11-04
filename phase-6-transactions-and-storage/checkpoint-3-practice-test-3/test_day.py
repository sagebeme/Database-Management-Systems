"""Checkpoint 3: Practice Test 3. Each question is one test; your score is the marks of the ones that pass.

The answers are stored as SHA-256 hashes, so reading this file won't give them away.
"""

import hashlib

import pytest

from coursekit import load_module

ANSWER_HASHES = {
    1: "b17e80c54f8f484a70c6dc1c17b902b6765ff27adc789700f724e4b2b3df98e7",
    2: "c35176eb476efe719d4ff25a89d79256998c8542451f3b292e8c3f093f0de10e",
    3: "3671a771925a5d5a26f530c3252e1ed80130d907823db2b9090d244617689346",
    4: "7646cbaee931dd266d35a6ec3e2c465f3887330be119b21a984847a3d51f2c12",
    5: "68101ef9442d5acfce7660fe86a4d3cdc8c8f3e245b2f147b7b49152189064c5",
    6: "46aac5b56353854554cc3c7a3f69130ec606860e5f06307836643e039792ecc3",
    7: "248a90b06809f286a6dd07632053309f97dfc7a2bae8d40d59f9ac6203f63471",
    8: "1e330587ebce84e6882369dfdc20a13f65245b4310d4fe2406b407c07a64af1c",
    9: "18870dd6b6f70deb3f2309eb11b36890fd22353455b18f971878debcd7647ceb",
    10: "c64e5940442ed770dfad4389eaef284ebce55074bd2699d11ad593255301f1bd",
    11: "cfae1c1fdade459678faf5845673314fabbadd2b28683e0b66d079ef409dfcf5",
    12: "85c2eb93e679b83dc26c10adf37f00c92bc0695db69af68c93558e7a81f87f26",
    13: "e889ca615e22647f63d53f0d208877808e9da19dc141075e3ed8f83d7040d941",
    14: "acb793a5c32f8dba63132febd8cd08cc2b5bd007f53a97ec4a9a67731072087b",
    15: "b788d8d74dd90126262b6a869136c3c267882a65776d1b5e0b35c991d1a10c7b",
    16: "a883e6daa17411fdc623adb3e05a0b5e26bfe30b8c666c7dfc71e9d74cdb5230",
}
MARKS = {1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 1, 10: 2, 11: 2, 12: 2, 13: 2, 14: 1, 15: 1, 16: 2}


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
    digest = hashlib.sha256(f"cp3:{question}:{normalise(given)}".encode()).hexdigest()
    assert digest == ANSWER_HASHES[question], f"Q{question} ({MARKS[question]} marks): not this one"
