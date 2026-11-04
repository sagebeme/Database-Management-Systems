"""Day 99: The Final Exam. Each question is one test; your score is the marks of the ones that pass.

The answers are stored as SHA-256 hashes, so reading this file won't give them away.
"""

import hashlib

import pytest

from coursekit import load_module

ANSWER_HASHES = {
    1: "e84ee96cb9bb7e6cfbe45c0bffee540416cac96d4d6a3b060cca2a5d88edce40",
    2: "2ae34c8fb83f3882e90a6fe62d9fbd543531bf117a4a504ae948585828ec75c8",
    3: "ce9de33dc958afd76c3d3afdea3980291b708196337f162e25a99d36e2934ac2",
    4: "0f8d2956bdd54cab21bf43ff755e57c57134dc41f9f841f940f42a1c3abc404f",
    5: "e8528c9b1d8f50b419106cd39ced1b4bdceb8c17d80bf884e78803a60784750f",
    6: "4450048b928dd069c8fb5877f38df4ca64099df64128e3bd686fa8ad89d76afd",
    7: "050661a13168b09c47d17cc8a54bba244c204f69857c0896178578df11f0448f",
    8: "bf1a5a3717c8d7925fb307274f595a30f63cac29ea6dd3881c7e81e235273845",
    9: "03a01346d19990454749a2c93bc2d67741ea5740528373f4bac5d61bc76dc94c",
    10: "977d732fba9b1048f89b8e03f26287b3b1c63810493b5ffd280f4e5f820afd6a",
    11: "03ee76005b9722d7de7871ba1aa341139d43df90e450da8947ef9e88127ee413",
    12: "fce561c719143d65c196b8c68d18d0ae0d9502938fb1d02172ae4ed5b720d52d",
    13: "15127fa3931f582b9f9553ec30c3662a2d5db7e3c9c0d637b1785795311c4757",
    14: "27cf042644867f56bf8f6bc3b20fba6815b09ed37321624429416aedc7cfed49",
    15: "381e03b0908ca020bd2a81dbff3d89045c17fe82662ad3ff240fd1f665b60e2c",
    16: "ceec5dfc6c26c724d6d43d96129aa3865d6007cba410a6f9c1a90522d6f0851d",
    17: "350742adc4142850d8a3b7137026a2986e4bb2c329da44fefe81e4c550e08917",
    18: "5ff624ddcbe329ed42f31fb64dd9c32b6fae67fdd39058a500d197f121ecddf0",
    19: "741aa0e51c00400c1c3044afe4755ef81d39c20f0c0b23770d36b4f2d2e3be7c",
    20: "967caf0e4b177633190329299cc253869b3ae965785bd89492a466ed2fcb40c2",
    21: "5b7ed544bf5b2a98be827855dd2810ef7e1b0850702210b1eae071fcca4e8780",
    22: "214959667af5e1ff866798772733e25d6156d8d387727e25649ade9531333611",
    23: "590e14101ef8ff9c220e546109a113d1580c614924e21b5afbddf53d4594b139",
    24: "12f820ec2ab8781f6856c12def4a0e6f6d49893a9d67182ee0dd1745b5167baf",
    25: "032a2084a31eeb12faf6bb0307da0c9b447732f55e8c27790f50d34045086758",
    26: "c9af2cba2bb5589022c3ecfb7f280df8917da829477af97ef7ec005bac877d69",
    27: "a9df46d7965d6657849ea615c6a14860967e27aff4e1246dedafefb2265cdcc3",
    28: "8b7401b638c7df674149b4006d05696fd6f3871b6bf24f089eb32807f6a60f2c",
    29: "d86df5f601e261b1e6e8adec9f784c719546ee737693c7bde915c1e484b531b0",
    30: "8bd8717d2d661baa35393461c26d2b15f1cc9f6cb42268c7f2258dda6b40980c",
}
MARKS = {1: 1, 2: 1, 3: 2, 4: 1, 5: 2, 6: 2, 7: 1, 8: 2, 9: 1, 10: 2, 11: 2, 12: 2, 13: 1, 14: 2, 15: 1, 16: 1, 17: 1, 18: 2, 19: 2, 20: 2, 21: 2, 22: 2, 23: 1, 24: 2, 25: 1, 26: 2, 27: 2, 28: 1, 29: 1, 30: 1}


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
    digest = hashlib.sha256(f"day99:{question}:{normalise(given)}".encode()).hexdigest()
    assert digest == ANSWER_HASHES[question], f"Q{question} ({MARKS[question]} marks): not this one"


def test_kata_gate_score(target):
    from fractions import Fraction

    m = load_module(target / "marking.py")
    paper = {1: ("MCQ", 1, "B"), 2: ("MCQ", 2, "C"), 3: ("MSQ", 2, {"A", "C"}), 4: ("NAT", 2, 57), 5: ("NAT", 1, 7)}
    assert m.gate_score(paper, {}) == 0, "a blank paper scores nothing"
    assert m.gate_score(paper, {1: "b", 2: "C", 3: {"C", "A"}, 4: 57, 5: 7}) == 8
    assert m.gate_score(paper, {1: "A", 2: "C"}) == Fraction(5, 3), "a wrong 1-mark MCQ costs a third"
    assert m.gate_score(paper, {1: "A", 2: "D", 3: {"A"}, 4: 56, 5: None}) == -1, "wrong MSQ and NAT cost nothing"
    assert isinstance(m.gate_score(paper, {1: "A"}), Fraction), "keep it exact: thirds don't fit in a float"
