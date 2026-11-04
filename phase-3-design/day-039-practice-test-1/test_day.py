"""Day 39: Practice Test 1. Each question is one test; your score is the number that pass.

The answers are stored as SHA-256 hashes, so reading this file won't give them away.
"""

import hashlib

import pytest

from coursekit import load_module

ANSWER_HASHES = {
    1: "6f9b15d0f20f19cac2a1d200f3a2c409bc90174bdfba03cba9f0f05646693f67",
    2: "6d4e1a9623db1c853d583940fd726d6a52b954fa2e8ae8383c307d446b6e4b34",
    3: "1a0fe7e251797209f2bad4758c3ba06107199beea4cbd91a0a66c1a36da2417c",
    4: "e70d0936b6cb2d4221716206a59c927c198c82af3bf7523d74cfb6f54c342ef8",
    5: "f752a33e100cde2de057385015fa98955e4807261419583b48be4dca6dd80893",
    6: "22ba71c66fb8155a56e806e0462e727b1fb921c7d9b0952d07c2c5124d7d5fb6",
    7: "2af2253845764a56f67ad3bec282a1d527cf5b84b7b1317727126349e35c7117",
    8: "cc90d70f2742e73e8807d95435628a83b49e2136cb190229d8da809207485754",
    9: "946c7ec34a28478c825f2a4219ee5eff94fb7e15a21b2e2f5c6dd0399e8cb38f",
    10: "a2308ba0593e52b2e9dc513a230c6edb41e70771d38b0cb8d756c5c77c6c1086",
    11: "cd7800cf6f94a3316c10732098cb50dbe8a2f8f352a3791d7c620ed95480b3bb",
    12: "a34876f6cd8ee3134eb1dca77a38e2ad0987fc44646dc3b496e012dcf47d3684",
    13: "cf67a586db2b27351e46cd85b4b6f459c62736eb305dc5224f8c3eb16abee33b",
    14: "31ec138539b1c272c1cfbab0ef464dd52fa14e8885207c023d673a22fecd1fe0",
    15: "912ffbe1f279acfab6b574ffc3ad7ce0894cf4950a8ada0157a1532c7a6a6ed7",
    16: "261a5430043a19c58546c5e65a46388fc8cf48ffddb70e728d2a1add25d5cfaf",
}
MARKS = {1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 1, 7: 2, 8: 1, 9: 2, 10: 1, 11: 2, 12: 1, 13: 2, 14: 2, 15: 1, 16: 2}


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
    digest = hashlib.sha256(f"day39:{question}:{normalise(given)}".encode()).hexdigest()
    assert digest == ANSWER_HASHES[question], f"Q{question} ({MARKS[question]} marks): not this one"
