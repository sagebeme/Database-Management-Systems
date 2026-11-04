"""Extra: Predict the Output. Each question is one test; your score is the marks of the ones that pass.

The answers are stored as SHA-256 hashes, so reading this file won't give them away.
"""

import hashlib

import pytest

from coursekit import load_module

ANSWER_HASHES = {
    1: "8c8a64f170e054dba7e85270c430a88c4751ceb51eb4659099dabcfea3a2cf11",
    2: "89adafcf3069511be35db69db7ea35d50887336372e80b47a2d3611b53f4a5d3",
    3: "c46be2524fbd0e8a6b93d248b90f985666226849af3f92c21b6d50f5c57e861a",
    4: "e5c9e7464dffcae32330c1037f50a53637fa348be2b529d6d83b564d3f3bc33e",
    5: "87d3a6c97d6ba5d2b7c496662f0f922a1641f0098a3e0c5f1f46ae72347b7100",
    6: "b8f49e84aa20efa02e7f770e63c9d09adb9c8de252086beec2469b67b990e16a",
    7: "d6d129f6773ee1024034902586b259a3c38eb20bf6f6a4e5e53f4df317c23442",
    8: "1867ee416d468756443e4b22aa13edcaf370d3aae2665abf0d34d7d739443c38",
    9: "8dd783999aae07a51efaf4198fe5215a1833967fe39ce9ab6835f0506b81dd57",
    10: "a4c65e7577d6bc67f8e0348b5e17bc5c0eac054c443a983d19adc4d73ac66973",
    11: "9ba682967f7a674c2e57f06c43889b3a12c93ac4f9f5eff8e6cfed43013f85f9",
    12: "1cafaec5c184cfc807ec271e06d62b94dd2ced9c106ff4504071f41179a9a7fb",
    13: "736258c99c19de16ba7ab3cff2931cf32af050b29fcb476a00f9a1970b8798f9",
    14: "fbd7587ef5212b847ec1c7c85215f1d16b6aa4f4107051b47b47e4c7d0b0bf54",
    15: "22d1797b44057dbb72f20af805c0515d9fd943ccef0b2fe80e63feecc88f2e4c",
    16: "6df4b9020d46fc4bde47a54d9c5874584b87e3e841f9937633cbaf551178d884",
    17: "a27821cb4709d5c7af153f4fb78472b70a754343c6579986f9862f1b8c822f46",
}
MARKS = {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1}


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
    digest = hashlib.sha256(f"pto:{question}:{normalise(given)}".encode()).hexdigest()
    assert digest == ANSWER_HASHES[question], f"Q{question} ({MARKS[question]} marks): not this one"
